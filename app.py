from flask import Flask, render_template, request, session, redirect, url_for, jsonify, g
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import x 
import time
import uuid
import os
import dictionary
import requests
import io
import csv
import json

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)

# Set the maximum file size to 10 MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024   # 1 MB

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
 
 
##############################
@app.before_request
def load_g_user():
    g.user = session.get("user")


##############################
##############################
##############################
def _____USER_____(): pass 
##############################
##############################
##############################

@app.get("/")
def view_index():
   
    return render_template("index.html")

##############################
@app.context_processor
def global_variables():
    return dict (
        dictionary = dictionary,
        x = x
    )

##############################
@app.route("/login", methods=["GET", "POST"])
@app.route("/login/<lan>", methods=["GET", "POST"])
@x.no_cache
def login(lan = "english"):

    if lan not in x.allowed_languages: lan = "english"
    x.default_language = lan

    if request.method == "GET":
        if session.get("user", ""): return redirect(url_for("home"))
        return render_template("login.html", lan=lan)

    if request.method == "POST":
        try:
            # Validate           
            user_email = x.validate_user_email(lan)
            user_password = x.validate_user_password(lan)
            # Connect to the database
            q = "SELECT * FROM users WHERE user_email = %s"
            db, cursor = x.db()
            cursor.execute(q, (user_email,))
            user = cursor.fetchone()
            if not user: raise Exception(x.lans("user_not_found"), 400)

            if user["user_deleted_at"] != 0:
                 raise Exception(x.lans("user_not_found"), 400)

            if user.get("user_blocked_at") != 0:
                raise Exception(x.lans("user_not_found"), 400)

            if not check_password_hash(user["user_password"], user_password):
                raise Exception(x.lans("invalid_credentials"), 400)

            if user["user_verification_key"] != "":
                raise Exception(x.lans("user_not_verified"), 400)

            user.pop("user_password")
            user["user_language"] = lan

            session["user"] = user
            return f"""<browser mix-redirect="/home"></browser>"""

        except Exception as ex:
            ic(ex)

            # User errors
            if ex.args[1] == 400:
                toast_error = render_template("___toast_error.html", message=ex.args[0])
                return f"""<browser mix-update="#toast">{ toast_error }</browser>""", 400

            # System or developer error
            toast_error = render_template("___toast_error.html", message=f"{x.lans('system_under_maintenance')}")
            return f"""<browser mix-bottom="#toast">{ toast_error }</browser>""", 500

        finally:
            if "cursor" in locals(): cursor.close()
            if "db" in locals(): db.close()




##############################
@app.route("/signup", methods=["GET", "POST"])
@app.route("/signup/<lan>", methods=["GET", "POST"])
def signup(lan = "english"):

    if lan not in x.allowed_languages: lan = "english"
    x.default_language = lan


    if request.method == "GET":
        return render_template("signup.html", lan=lan)

    if request.method == "POST":
        try:
            # Validate
            user_email = x.validate_user_email(lan)
            user_password = x.validate_user_password(lan)
            user_username = x.validate_user_username()
            user_first_name = x.validate_user_first_name()

            user_pk = uuid.uuid4().hex
            user_last_name = ""
            user_avatar_path = "https://avatar.iran.liara.run/public/40"
            user_verification_key = uuid.uuid4().hex
            user_verified_at = 0
            user_deleted_at = 0

            user_hashed_password = generate_password_hash(user_password)

            # Connect to the database
            q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            db, cursor = x.db()
            cursor.execute(q, (user_pk, user_email, user_hashed_password, user_username, 
            user_first_name, user_last_name, user_avatar_path, user_verification_key, user_verified_at, user_deleted_at))
            db.commit()

            # send verification email
            email_verify_account = render_template("_email_verify_account.html", user_verification_key=user_verification_key)
            # ic(email_verify_account)
            x.send_email(user_email, "Verify your account", email_verify_account)

            return f"""<mixhtml mix-redirect="{ url_for('login') }"></mixhtml>""", 400
        except Exception as ex:
            ic(ex)
            # User errors
            if ex.args[1] == 400:
                toast_error = render_template("___toast_error.html", message=ex.args[0])
                return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
            
            # Database errors
            if "Duplicate entry" and user_email in str(ex): 
                toast_error = render_template("___toast_error.html", message=f"{x.lans('email_already_registered')}")
                return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
            if "Duplicate entry" and user_username in str(ex): 
                toast_error = render_template("___toast_error.html", message=f"{x.lans('username_already_registered')}")
                return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
            
            # System or developer error
            toast_error = render_template("___toast_error.html", message=f"{x.lans('system_under_maintenance')}")
            return f"""<mixhtml mix-bottom="#toast">{ toast_error }</mixhtml>""", 500

        finally:
            if "cursor" in locals(): cursor.close()
            if "db" in locals(): db.close()



##############################
@app.get("/home")
@x.no_cache
def home():
    try:
        user = session.get("user", "")
        if not user: return redirect(url_for("login"))
        user_pk = user["user_pk"]
        
        db, cursor = x.db()

        # Fetch tweets, total likes, and current user's like status in one query
        q = """
            SELECT 
                p.post_pk, p.post_message, p.post_image_path, p.post_total_likes, 
                u.user_first_name, u.user_last_name, u.user_username, u.user_avatar_path,
                (SELECT COUNT(*) FROM likes WHERE like_post_fk = p.post_pk AND like_user_fk = %s) AS is_liked_by_user
            FROM posts p
            JOIN users u ON u.user_pk = p.post_user_fk 
            WHERE p.post_blocked_at = 0
            ORDER BY RAND() LIMIT 5
        """
        cursor.execute(q, (user_pk,))
        tweets = cursor.fetchall()
        
        # Convert the count to a boolean for template logic
        for tweet in tweets:
            tweet['is_liked_by_user'] = True if tweet['is_liked_by_user'] > 0 else False
            
        # ic(tweets)

        q = "SELECT * FROM trends ORDER BY RAND() LIMIT 3"
        cursor.execute(q)
        trends = cursor.fetchall()
        # ic(trends)

        # Suggestions query to check if already followed
        q = """
            SELECT users.*, 
            (SELECT COUNT(*) FROM follows WHERE follow_follower_fk = %s AND follow_followed_fk = users.user_pk) AS is_followed_by_user
            FROM users users 
            WHERE users.user_pk != %s 
            AND users.user_pk NOT IN (SELECT follow_followed_fk FROM follows WHERE follow_follower_fk = %s)
            ORDER BY RAND() LIMIT 5
        """
        cursor.execute(q, (user_pk, user_pk, user_pk))
        suggestions = cursor.fetchall()

        # Convert 1/0 to Boolean for Jinja
        for suggestion in suggestions:
            suggestion['is_followed_by_user'] = True if suggestion['is_followed_by_user'] > 0 else False
            suggestion.pop("user_password", None)
        
        # Following query to get users that the current user is following
        q = """
            SELECT 
                users.*, 
                (SELECT COUNT(*) FROM follows WHERE follow_follower_fk = %s AND follow_followed_fk = users.user_pk) AS is_followed_by_user
            FROM users users
            JOIN follows ON users.user_pk = follows.follow_followed_fk 
            WHERE follows.follow_follower_fk = %s
        """
        cursor.execute(q, (user_pk, user_pk))
        following = cursor.fetchall()

         # Convert 1/0 to Boolean for Jinja
        for follow in following:
            follow['is_followed_by_user'] = True if follow['is_followed_by_user'] > 0 else False
            follow.pop("user_password", None)

        lan = session["user"]["user_language"]

        return render_template("home.html", lan=lan, dictionary=dictionary, tweets=tweets, trends=trends, suggestions=suggestions, following=following, user=user)
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.route("/verify-account", methods=["GET"])
def verify_account():
    try:
        user_verification_key = x.validate_uuid4_without_dashes(request.args.get("key", ""))
        user_verified_at = int(time.time())
        db, cursor = x.db()
        q = "UPDATE users SET user_verification_key = '', user_verified_at = %s WHERE user_verification_key = %s"
        cursor.execute(q, (user_verified_at, user_verification_key))
        db.commit()
        if cursor.rowcount != 1: raise Exception("Invalid key", 400)
        return redirect( url_for('login') )
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        # User errors
        if ex.args[1] == 400: return ex.args[0], 400    

        # System or developer error
        return "Cannot verify user"

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/logout")
def logout():
    try:
        session.clear()
        return redirect(url_for("login"))
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass



##############################
@app.get("/home-comp")
def home_comp():
    try:

        user = session.get("user", "")
        if not user: return "error"
        db, cursor = x.db()
        q = "SELECT * FROM users JOIN posts ON user_pk = post_user_fk WHERE posts.post_blocked_at = 0 ORDER BY RAND() LIMIT 5"
        cursor.execute(q)
        tweets = cursor.fetchall()
        # ic(tweets)

        html = render_template("_home_comp.html", tweets=tweets, user=user)
        return f"""<browser mix-update="main">{ html }</browser>"""
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass


##############################
@app.get("/profile")
def profile():
    try:
        user = session.get("user", "")
        if not user: return "error"
        q = "SELECT * FROM users WHERE user_pk = %s"
        db, cursor = x.db()
        cursor.execute(q, (user["user_pk"],))
        user = cursor.fetchone()
        lan = session["user"]["user_language"]
        profile_html = render_template("_profile.html", x=x, user=user, lan=lan, dictionary=dictionary)
        return f"""<browser mix-update="main">{ profile_html }</browser>"""
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass


##############################
@app.get("/admin")
def admin():
    try:
        user = session.get("user", "")
        if not user: return redirect(url_for("login"))
        
        # Only allow admins; others go back to home
        if not user.get("user_is_admin"):
            return redirect(url_for("home"))

        lan = session["user"]["user_language"]
        
        # Get all non-admin users
        db, cursor = x.db()
        q = """
        SELECT user_pk, user_username, user_first_name, user_blocked_at
        FROM users
        WHERE user_is_admin = 0
        ORDER BY user_username
        """
        cursor.execute(q)
        users = cursor.fetchall()

        html = render_template("_admin.html", user=user, users=users, lan=lan, x=x)
        return f"""<browser mix-update="main">{ html }</browser>"""
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/admin-users-section")
def admin_users_section():
    try:
        user = session.get("user", "")
        if not user:
            return redirect(url_for("login"))

        if not user.get("user_is_admin"):
            return redirect(url_for("home"))

        db, cursor = x.db()
        q = """
        SELECT user_pk, user_username, user_first_name, user_blocked_at
        FROM users
        WHERE user_is_admin = 0
        ORDER BY user_username
        """
        cursor.execute(q)
        users = cursor.fetchall()

        nav_html = render_template("___admin_nav.html")
        content_html = render_template("_admin_users.html", users=users, user=user, x=x)

        return f"""
        <browser mix-update="#admin_nav">{ nav_html }</browser>
        <browser mix-update="#admin_content">{ content_html }</browser>
        """
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/admin-posts-section")
def admin_posts_section():
    try:
        user = session.get("user", "")
        if not user:
            return redirect(url_for("login"))

        if not user.get("user_is_admin"):
            return redirect(url_for("home"))

        db, cursor = x.db()

        # Get blocked posts with user fields and like status like the home feed
        user_pk = user["user_pk"]
        q = """
            SELECT 
                p.post_pk,
                p.post_message,
                p.post_image_path,
                p.post_total_likes,
                p.post_blocked_at,
                u.user_first_name,
                u.user_last_name,
                u.user_username,
                u.user_avatar_path,
                (
                    SELECT COUNT(*) 
                    FROM likes 
                    WHERE like_post_fk = p.post_pk AND like_user_fk = %s
                ) AS is_liked_by_user
            FROM posts p
            JOIN users u ON u.user_pk = p.post_user_fk 
            WHERE p.post_blocked_at != 0
            ORDER BY p.post_blocked_at DESC
        """
        cursor.execute(q, (user_pk,))
        blocked_posts = cursor.fetchall()

        content_html = render_template("_admin_posts.html", blocked_posts=blocked_posts, user=user, x=x)
        nav_html = render_template("___admin_nav.html")

        return f"""
        <browser mix-update="#admin_nav">{ nav_html }</browser>
        <browser mix-update="#admin_content">{ content_html }</browser>
        """
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/api-admin-block-user")
def api_admin_block_user():
    try:
        admin_user = session.get("user", "")
        if not admin_user: return "invalid user", 401
        if not admin_user.get("user_is_admin"): return "forbidden", 403

        username = request.form.get("user_username", "").strip()
        user_pk = request.form.get("user_pk", "").strip()
        if not username: return "missing username", 400
        if not user_pk: return "missing user_pk", 400

        
        db, cursor = x.db()
        cursor.execute("UPDATE users SET user_blocked_at = %s WHERE user_pk = %s", (int(time.time()), user_pk))
        db.commit()

        try:
            cursor.execute("SELECT user_email FROM users WHERE user_pk = %s", (user_pk,))
            user_row = cursor.fetchone()
            if user_row and user_row.get("user_email"):
                blocked_email = user_row["user_email"]
                subject = "Your account has been blocked"
                body = f"""
                <p>Hello {username},</p>
                <p>Your account has been blocked by an administrator.</p>
                <p>If you believe this is a mistake, please contact support.</p>
                """
                x.send_email(blocked_email, subject, body)
        except Exception as email_ex:
            ic(f"Failed to send block email: {email_ex}")

        btn_html = render_template("___button_unblock_user.html", user_username=username, user_pk=user_pk)
        toast_ok = render_template("___toast_ok.html", message=x.lans('toast_user_blocked'))
        return f"""
            <browser mix-bottom="#toast">{toast_ok}</browser>
            <mixhtml mix-replace="#admin_btn_{user_pk}">{btn_html}</mixhtml>
        """, 200
    except Exception as ex:
        ic(ex)
        return "error", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.post("/api-admin-unblock-user")
def api_admin_unblock_user():
    try:
        admin_user = session.get("user", "")
        if not admin_user: return "invalid user", 401
        if not admin_user.get("user_is_admin"): return "forbidden", 403

        username = request.form.get("user_username", "").strip()
        user_pk = request.form.get("user_pk", "").strip()
        if not username: return "missing username", 400
        if not user_pk: return "missing user_pk", 400

        # Persist: reset blocked timestamp
        db, cursor = x.db()
        cursor.execute("UPDATE users SET user_blocked_at = 0 WHERE user_pk = %s", (user_pk,))
        db.commit()

        try:
            cursor.execute("SELECT user_email FROM users WHERE user_pk = %s", (user_pk,))
            user_row = cursor.fetchone()
            if user_row and user_row.get("user_email"):
                unblocked_email = user_row["user_email"]
                subject = "Your account has been unblocked"
                body = f"""
                <p>Hello {username},</p>
                <p>Your account has been unblocked by an administrator.</p>
                <p>You can now login to the account again</p>
                """
                x.send_email(unblocked_email, subject, body)
        except Exception as email_ex:
            ic(f"Failed to send unblock email: {email_ex}")

        btn_html = render_template("___button_block_user.html", user_username=username, user_pk=user_pk)
        toast_ok = render_template("___toast_ok.html", message=x.lans('toast_user_unblocked'))
        return f"""
            <browser mix-bottom="#toast">{toast_ok}</browser>
            <mixhtml mix-replace="#admin_btn_{user_pk}">{btn_html}</mixhtml>
        """, 200
    except Exception as ex:
        ic(ex)
        return "error", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.post("/api-admin-block-post")
def api_admin_block_post():
    try:
        admin_user = session.get("user", "")
        if not admin_user or not admin_user.get("user_is_admin"):
            return "forbidden", 403

        post_pk = request.form.get("post_pk", "")
        if not post_pk:
            return "missing post_pk", 400

        db, cursor = x.db()
        cursor.execute("UPDATE posts SET post_blocked_at = %s WHERE post_pk = %s", (int(time.time()), post_pk))
        db.commit()

        try:
            cursor.execute(
                """
                SELECT u.user_email, u.user_username, p.post_message, p.post_created_at
                FROM posts p
                JOIN users u ON u.user_pk = p.post_user_fk
                WHERE p.post_pk = %s
                """,
                (post_pk,)
            )
            post_row = cursor.fetchone()
            if post_row and post_row.get("user_email"):
                blocked_email = post_row["user_email"]
                subject = "Your post has been blocked"
                body = f"""
                <p>Hello @{post_row.get('user_username', '')},</p>
                <p>Your post has been blocked by an administrator.</p>
                <p><strong>Message:</strong><br>{post_row.get('post_message', '')}</p>
                <p><strong>Posted at:</strong> {post_row.get('post_created_at', '')}</p>
                <p>If you believe this is a mistake, please contact support.</p>
                """
                x.send_email(blocked_email, subject, body)
        except Exception as email_ex:
            ic(f"Failed to send post blocked email: {email_ex}")
        
        btn_html = render_template("___button_unblock_post.html", post_pk=post_pk)
        toast_ok = render_template("___toast_ok.html", message=x.lans('toast_post_blocked'))
        return f"""
            <browser mix-bottom=\"#toast\">{toast_ok}</browser>
            <mixhtml mix-replace=\"#block-btn-{post_pk}\">{btn_html}</mixhtml>
        """, 200
    except Exception as ex:
        ic(ex)
        return "error", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.post("/api-admin-unblock-post")
def api_admin_unblock_post():
    try:
        admin_user = session.get("user", "")
        if not admin_user or not admin_user.get("user_is_admin"):
            return "forbidden", 403

        post_pk = request.form.get("post_pk", "")
        if not post_pk:
            return "missing post_pk", 400

        source = request.form.get("source", "")

        db, cursor = x.db()
        cursor.execute("UPDATE posts SET post_blocked_at = 0 WHERE post_pk = %s", (post_pk,))
        db.commit()

        try:
            cursor.execute(
                """
                SELECT u.user_email, u.user_username, p.post_message, p.post_created_at
                FROM posts p
                JOIN users u ON u.user_pk = p.post_user_fk
                WHERE p.post_pk = %s
                """,
                (post_pk,)
            )
            post_row = cursor.fetchone()
            if post_row and post_row.get("user_email"):
                unblocked_email = post_row["user_email"]
                subject = "Your post has been unblocked"
                body = f"""
                <p>Hello @{post_row.get('user_username', '')},</p>
                <p>Your post has been unblocked by an administrator.</p>
                <p><strong>Message:</strong><br>{post_row.get('post_message', '')}</p>
                <p><strong>Posted at:</strong> {post_row.get('post_created_at', '')}</p>
                <p>You can now view it again.</p>
                """
                x.send_email(unblocked_email, subject, body)
        except Exception as email_ex:
            ic(f"Failed to send post unblocked email: {email_ex}")

        toast_ok = render_template("___toast_ok.html", message=x.lans('toast_post_unblocked'))
        btn_html = render_template("___button_block_post.html", post_pk=post_pk)
        return f"""
            <browser mix-bottom=\"#toast\">{toast_ok}</browser>
            <mixhtml mix-replace=\"#block-btn-{post_pk}\">{btn_html}</mixhtml>
        """, 200
    except Exception as ex:
        ic(ex)
        return "error", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.patch("/like-tweet")
@x.no_cache
def api_like_tweet():
    try:
        user = session.get("user", "")
        if not user: return "invalid user", 401
        
        post_pk = request.form.get("post_pk", "") 
        if not post_pk: raise Exception("Missing post ID", 400)

        user_pk = user["user_pk"]
        
        # Get the current Unix epoch timestamp in seconds
        current_epoch = int(time.time()) 

        db, cursor = x.db()

        # Insert a new like record with the composite key and timestamp
        q_insert_like = "INSERT INTO likes (like_user_fk, like_post_fk, like_timestamp) VALUES(%s, %s, %s)"
        cursor.execute(q_insert_like, (user_pk, post_pk, current_epoch))
        
        db.commit()
        
        # Get the new total like count to display
        q_get_count = "SELECT post_total_likes FROM posts WHERE post_pk = %s"
        cursor.execute(q_get_count, (post_pk,))
        new_count = cursor.fetchone()["post_total_likes"]

        # Response to the browser: replace button and update count
        button_unlike_tweet = render_template("___button_unlike_tweet.html", post_pk=post_pk, like_count=new_count)
        
        return f"""
            <mixhtml mix-replace="#button_container_{post_pk}">
                {button_unlike_tweet}
            </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        # If already liked (Duplicate entry), just return OK with the unlike button
        if "Duplicate entry" in str(ex):
            # This is a fallback in case the frontend logic fails to use the correct button
            # We must fetch the current count to return the correct unlike button
            try:
                db, cursor = x.db()
                q_get_count = "SELECT post_total_likes FROM posts WHERE post_pk = %s"
                cursor.execute(q_get_count, (post_pk,))
                current_count = cursor.fetchone()["post_total_likes"]
                button_unlike_tweet = render_template("___button_unlike_tweet.html", post_pk=post_pk, like_count=current_count)
                return f"""<mixhtml mix-replace="#button_container_{post_pk}">{button_unlike_tweet}</mixhtml>"""
            except:
                return "Already liked, failed to get count", 400
        
        # Other errors
        if ex.args and len(ex.args) > 1 and ex.args[1] == 400:
            return ex.args[0], 400

        return "System error during like", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.patch("/unlike-tweet")
@x.no_cache
def api_unlike_tweet():
    try:
        user = session.get("user", "")
        if not user: return "invalid user", 401
        
        # Get post_pk from mix-data form
        post_pk = request.form.get("post_pk", "") 
        if not post_pk: raise Exception("Missing post ID", 400)

        user_pk = user["user_pk"]

        db, cursor = x.db()

        # Delete the like record
        q_delete_like = "DELETE FROM likes WHERE like_user_fk = %s AND like_post_fk = %s"
        cursor.execute(q_delete_like, (user_pk, post_pk))
        db.commit()

       # Get the new total like count to display
        q_get_count = "SELECT post_total_likes FROM posts WHERE post_pk = %s"
        cursor.execute(q_get_count, (post_pk,))
        new_count = cursor.fetchone()["post_total_likes"]

        # Response to the browser: replace button and update count
        button_like_tweet = render_template("___button_like_tweet.html", post_pk=post_pk, like_count=new_count)
        
        return f"""
            <mixhtml mix-replace="#button_container_{post_pk}">
                {button_like_tweet}
            </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()

        # User errors
        if ex.args and len(ex.args) > 1 and ex.args[1] == 400:
            return ex.args[0], 400

        return "System error during unlike", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.post("/follow-user")
@x.no_cache
def follow_user():
    try:
        user = session.get("user")
        if not user: return "unauthorized", 401
        
        follower_fk = user["user_pk"]
        followed_fk = request.form.get("user_pk")
        
        if not followed_fk: raise Exception("User ID missing", 400)
        
        db, cursor = x.db()
        
        # Insert into follows table
        q = "INSERT INTO follows (follow_follower_fk, follow_followed_fk, follow_timestamp) VALUES (%s, %s, %s)"
        cursor.execute(q, (follower_fk, followed_fk, int(time.time())))
        db.commit()
        
        # Return the Unfollow button to swap in the UI
        btn = render_template("___button_unfollow.html", user_pk=followed_fk)
        return f"""<mixhtml mix-replace="#follow_btn_{followed_fk}">{btn}</mixhtml>"""

    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        # If already following, return success with Unfollow button to fix UI
        if "Duplicate entry" in str(ex):
            btn = render_template("___button_unfollow.html", user_pk=followed_fk)
            return f"""<mixhtml mix-replace="#follow_btn_{followed_fk}">{btn}</mixhtml>"""
        return "System Error", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.patch("/unfollow-user")
@x.no_cache
def unfollow_user():
    try:
        user = session.get("user")
        if not user: return "unauthorized", 401
        
        follower_fk = user["user_pk"]
        followed_fk = request.form.get("user_pk")
        
        if not followed_fk: raise Exception("User ID missing", 400)
        
        db, cursor = x.db()
        
        # Delete from follows table
        q = "DELETE FROM follows WHERE follow_follower_fk = %s AND follow_followed_fk = %s"
        cursor.execute(q, (follower_fk, followed_fk))
        db.commit()
        
        # Return the Follow button to swap in the UI
        btn = render_template("___button_follow.html", user_pk=followed_fk)
        return f"""<mixhtml mix-replace="#follow_btn_{followed_fk}">{btn}</mixhtml>"""

    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        return "System Error", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.route("/api-create-post", methods=["POST"])
def api_create_post():
    try:
        user = session.get("user", "")
        if not user: return "invalid user"
        user_pk = user["user_pk"]        
        post = x.validate_post(request.form.get("post", ""))
        post_pk = uuid.uuid4().hex
        post_image_path = ""
        db, cursor = x.db()
        q = "INSERT INTO posts VALUES(%s, %s, %s, %s, %s)"
        cursor.execute(q, (post_pk, user_pk, post, 0, post_image_path))
        db.commit()
        toast_ok = render_template("___toast_ok.html", message="The world is reading your post !")
        tweet = {
            "user_first_name": user["user_first_name"],
            "user_last_name": user["user_last_name"],
            "user_username": user["user_username"],
            "user_avatar_path": user["user_avatar_path"],
            "post_message": post,
        }
        html_post_container = render_template("___post_container.html")
        html_post = render_template("_tweet.html", tweet=tweet)
        return f"""
            <browser mix-bottom="#toast">{toast_ok}</browser>
            <browser mix-top="#posts">{html_post}</browser>
            <browser mix-replace="#post_container">{html_post_container}</browser>
        """
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()

        # User errors
        if "x-error post" in str(ex):
            toast_error = render_template("___toast_error.html", message=f"Post - {x.POST_MIN_LEN} to {x.POST_MAX_LEN} characters")
            return f"""<browser mix-bottom="#toast">{toast_error}</browser>"""

        # System or developer error
        toast_error = render_template("___toast_error.html", message="System under maintenance")
        return f"""<browser mix-bottom="#toast">{ toast_error }</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()   

##############################
@app.route("/api-update-post", methods=["POST"])
def api_update_post(): 
    try:
        pass
    except Exception as ex:
        pass
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



##############################
@app.route("/api-update-profile", methods=["POST"])
def api_update_profile():

    try:
        user = session.get("user", "")
        lan = session["user"]["user_language"]
        if not user: return "invalid user"

        # Validate
        user_email = x.validate_user_email(lan)
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()

        # Connect to the database
        q = """
        UPDATE users
        SET user_email = %s,
            user_username = %s,
            user_first_name = %s
        WHERE user_pk = %s
        """


        db, cursor = x.db()
        # Avatar is handled in /api-upload-avatar; pass None to keep current value via COALESCE
        cursor.execute(q, (user_email, user_username, user_first_name, user["user_pk"]))
        db.commit()

        # Update session minimally
        session["user"]["user_email"] = user_email
        session["user"]["user_username"] = user_username
        session["user"]["user_first_name"] = user_first_name

        # Response to the browser
      
        toast_ok = render_template("___toast_ok.html", message=f"{x.lans('profile_updated_successfully')}")
        return f"""
            <browser mix-bottom="#toast">{toast_ok}</browser>
            <browser mix-update="#profile_tag .name">{user_first_name}</browser>
            <browser mix-update="#profile_tag .handle">{user_username}</browser>
        """, 200
    except Exception as ex:
        ic(ex)
        # User errors
        if ex.args[1] == 400:
            toast_error = render_template("___toast_error.html", message=ex.args[0])
            return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
        
        # Database errors
        if "Duplicate entry" and user_email in str(ex): 
            toast_error = render_template("___toast_error.html", message=f"{x.lans('email_already_registered')}")
            return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
        if "Duplicate entry" and user_username in str(ex): 
            toast_error = render_template("___toast_error.html", message=f"{x.lans('username_already_registered')}")
            return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
        
        # System or developer error
        toast_error = render_template("___toast_error.html", message=f"{x.lans('system_under_maintenance')}")
        return f"""<mixhtml mix-bottom="#toast">{ toast_error }</mixhtml>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.route("/api-delete-profile", methods=["GET", "PUT"])
def api_delete_profile():
    try:
        user = session.get("user", "")
        if not user: return "invalid user"
        user_pk = user.get("user_pk")

        db, cursor = x.db()
        q = "UPDATE users SET user_deleted_at = %s WHere user_pk = %s"
        cursor.execute(q, (int(time.time()), user_pk))
        db.commit()
        
        session.clear()
        return redirect(url_for("login"))

    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        return "System under maintenance", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

# ##############################

##############################
@app.route("/api-upload-avatar", methods=["POST"])
def api_upload_avatar():
    """
    Handles avatar/profile picture upload
    """
    try:
        # Check if user is logged in
        if not g.get("user"):
            raise Exception("You must be logged in", 400)

        # Validate uploaded file
        if "avatar" not in request.files:
            raise Exception("missing file", 400)
        file = request.files["avatar"]
        if not file or not file.filename:
            raise Exception("missing filename", 400)
        allowed_ext = {"jpg", "jpeg", "png", "gif", "webp"}
        filename_original = file.filename
        if "." not in filename_original:
            raise Exception("invalid file type", 400)
        file_extension = filename_original.rsplit(".", 1)[-1].lower()
        if file_extension not in allowed_ext:
            raise Exception("invalid file type", 400)

        # Create unique filename with UUID
        unique_id = uuid.uuid4().hex
        filename = f"{unique_id}.{file_extension}"

        # Build filepath inside static/images/avatars
        filepath = os.path.join('static', 'images', 'avatars', filename)

        # Ensure avatars folder exists (absolute on disk)
        avatar_folder = os.path.join(app.root_path, 'static', 'images', 'avatars')
        if not os.path.exists(avatar_folder):
            os.makedirs(avatar_folder)

        # Delete old avatar if it exists (not external URL)
        if g.user.get("user_avatar_path") and not g.user["user_avatar_path"].startswith("http"):
            old_avatar = g.user["user_avatar_path"]  # e.g. static/images/avatars/abc.png
            fs_old = os.path.join(app.root_path, old_avatar.lstrip('/'))
            if os.path.exists(fs_old):
                try:
                    os.remove(fs_old)
                    ic(f"Deleted old avatar: {fs_old}")
                except Exception as e:
                    ic(f"Could not delete old avatar: {e}")

        # Save new file to disk
        file.save(os.path.join(app.root_path, filepath))

        # Update database
        db, cursor = x.db()
        q = "UPDATE users SET user_avatar_path = %s WHERE user_pk = %s"
        cursor.execute(q, (filepath, g.user["user_pk"]))
        db.commit()

        # Update g.user in memory
        g.user["user_avatar_path"] = filepath

        # Send success response and redirect
        toast_ok = render_template("___toast_ok.html", message="Avatar updated successfully!")

        avatar_url = f"/static/images/avatars/{filename}"
        return f"""
            <browser mix-bottom="#toast">{toast_ok}</browser>
            <browser mix-replace="#current_avatar"><img id=\"current_avatar\" src=\"{avatar_url}\" class=\"w-25 h-25 rounded-full obj-f-cover\" alt=\"Current avatar\"></browser>
            <browser mix-replace="#profile_avatar"><img id=\"profile_avatar\" src=\"{avatar_url}\" class=\"w-25 h-25 rounded-full obj-f-cover\" alt=\"Profile Picture\"></browser>
            <browser mix-replace="#nav_avatar"><img src=\"/{filepath}\" alt=\"Profile\" id=\"nav_avatar\"></browser>
        """, 200
    except Exception as ex:
        ic(f"Exception: {ex}")

        # Cleanup: delete uploaded file if error occurred
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)

        # Rollback database changes
        if "db" in locals(): 
            db.rollback()

        # User validation error
        if len(ex.args) > 1 and ex.args[1] == 400:
            toast_error = render_template("___toast_error.html", message=ex.args[0])
            return f"""<browser mix-bottom=\"#toast\">{toast_error}</browser>""", 400

        # System error
        toast_error = render_template("___toast_error.html", message=f"Could not upload avatar: {str(ex)}")
        return f"""<browser mix-bottom=\"#toast\">{toast_error}</browser>""", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


# @app.post("/api-search")
# def api_search():
#     try:
#         # TODO: The input search_for must be validated
#         search_for = request.form.get("search_for", "")
#         if not search_for:
#             return """
#             <browser mix-remove="#search_results"></browser>
#             """
#         part_of_query = f"%{search_for}%"
#         ic(search_for)
#         db, cursor = x.db()
#         q = "SELECT * FROM users WHERE user_username LIKE %s"
#         cursor.execute(q, (part_of_query,))
#         users = cursor.fetchall()
#         orange_box = render_template("_orange_box.html", users=users)
#         return f"""
#             <browser mix-remove="#search_results"></browser>
#             <browser mix-bottom="#search_form">{orange_box}</browser>
#         """
#     except Exception as ex:
#         ic(ex)
#         return str(ex)
#     finally:
#         if "cursor" in locals(): cursor.close()
#         if "db" in locals(): db.close()


##############################
@app.post("/api-search")
def api_search():
    try:
        # TODO: The input search_for must be validated
        search_for = request.form.get("search_for", "")
        if not search_for: return """empty search field""", 400
        part_of_query = f"%{search_for}%"
        # ic(search_for)
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_username LIKE %s"
        cursor.execute(q, (part_of_query,))
        users = cursor.fetchall()
        return jsonify(users)
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/get-data-from-sheet")
def get_data_from_sheet():
    try:
 
        # Check if the admin is running this end-point, else show error
        admin_user = session.get("user", "")
        if not admin_user:
            return redirect(url_for("login"))
        if not admin_user.get("user_is_admin"):
            return redirect(url_for("home"))
 
        # flaskwebmail
        # Create a google sheet
        # share and make it visible to "anyone with the link"
        # In the link, find the ID of the sheet. Here: 1aPqzumjNp0BwvKuYPBZwel88UO-OC_c9AEMFVsCw1qU
        # Replace the ID in the 2 places bellow
        url= f"https://docs.google.com/spreadsheets/d/{x.google_spread_sheet_key}/export?format=csv&id={x.google_spread_sheet_key}"
        res=requests.get(url=url)
        # ic(res.text) # contains the csv text structure
        csv_text = res.content.decode('utf-8')
        csv_file = io.StringIO(csv_text) # Use StringIO to treat the string as a file
       
        # Initialize an empty list to store the data
        data = {}
 
        # Read the CSV data
        reader = csv.DictReader(csv_file)
        # ic(reader)
        # Convert each row into the desired structure
        for row in reader:
            item = {
                    'english': row['english'],
                    'danish': row['danish'],
                    'spanish': row['spanish']
               
            }
            # Append the dictionary to the list
            data[row['key']] = (item)
 
        # Convert the data to JSON
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        # ic(data)
 
        # Save data to the file
        with open("dictionary.json", 'w', encoding='utf-8') as f:
            f.write(json_data)
 
        return "ok"
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        pass