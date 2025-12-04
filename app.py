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
from werkzeug.utils import secure_filename

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)

# Set the maximum file size to 10 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
 

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
    user = session.get("user", None)
    lan = user.get("user_language", "english") if user else "english"
    return dict(
        lan=lan,
        user=user,
        x=x,
        lans=x.lans,
        dictionary=dictionary
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
            user_email = x.validate_user_email()
            user_password = x.validate_user_password()
            user_username = x.validate_user_username()
            user_first_name = x.validate_user_first_name()

            user_pk = uuid.uuid4().hex
            user_last_name = ""
            user_avatar_path = "https://avatar.iran.liara.run/public/40"
            user_verification_key = uuid.uuid4().hex
            user_verified_at = 0

            user_hashed_password = generate_password_hash(user_password)

            # Connect to the database
            q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            db, cursor = x.db()
            cursor.execute(q, (user_pk, user_email, user_hashed_password, user_username, 
            user_first_name, user_last_name, user_avatar_path, user_verification_key, user_verified_at))
            db.commit()

            # send verification email
            email_verify_account = render_template("_email_verify_account.html", user_verification_key=user_verification_key)
            ic(email_verify_account)
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
        db, cursor = x.db()
        q = "SELECT * FROM users JOIN posts ON user_pk = post_user_fk ORDER BY RAND() LIMIT 5"
        cursor.execute(q)
        tweets = cursor.fetchall()
        ic(tweets)

        q = "SELECT * FROM trends ORDER BY RAND() LIMIT 3"
        cursor.execute(q)
        trends = cursor.fetchall()
        ic(trends)

        q = "SELECT * FROM users WHERE user_pk != %s ORDER BY RAND() LIMIT 3"
        cursor.execute(q, (user["user_pk"],))
        suggestions = cursor.fetchall()
        ic(suggestions)

        lan = session["user"]["user_language"]

        return render_template("home.html", lan=lan, dictionary=dictionary, tweets=tweets, trends=trends, suggestions=suggestions, user=user)
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
        q = "SELECT * FROM users JOIN posts ON user_pk = post_user_fk ORDER BY RAND() LIMIT 5"
        cursor.execute(q)
        tweets = cursor.fetchall()
        ic(tweets)

        html = render_template("_home_comp.html", tweets=tweets)
        return f"""<mixhtml mix-update="main">{ html }</mixhtml>"""
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
@app.patch("/like-tweet")
@x.no_cache
def api_like_tweet():
    try:
        button_unlike_tweet = render_template("___button_unlike_tweet.html")
        return f"""
            <mixhtml mix-replace="#button_1">
                {button_unlike_tweet}
            </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.route("/api-create-post", methods=["POST"])
def api_create_post():
    try:
        print("Files in request:", request.files)
        print("Form data:", request.form)

        user = session.get("user", "")
        if not user: return "invalid user"
        user_pk = user["user_pk"]        
        post = x.validate_post(request.form.get("post", ""))
        post_pk = uuid.uuid4().hex
        post_media_path = ""
        
        # Handle file upload
        if 'post_media' in request.files:
            file = request.files['post_media']
            if file and file.filename:
                # CHECK FILE SIZE FIRST (5MB limit) - THIS WAS MISSING!
                file.seek(0, 2)  # Seek to end
                size = file.tell()
                file.seek(0)  # Reset to beginning
                
                if size > 5 * 1024 * 1024:  # 5MB
                    raise Exception("x-error file size too large")
                
                # Validate file extension
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                
                if file_ext not in allowed_extensions:
                    raise Exception("x-error file invalid type")
                
                # Generate unique filename
                from werkzeug.utils import secure_filename
                original_filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{original_filename}"

                upload_dir = 'static/images'
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                    print(f"Created directory: {upload_dir}")
                
                # Save file
                file_path = os.path.join('static/images', unique_filename)
                file.save(file_path)
                
                # Store just the filename for database
                post_media_path = f"images/{unique_filename}"
        
        db, cursor = x.db()
        q = """INSERT INTO posts 
       (post_pk, post_user_fk, post_message, post_deleted_at, post_media_path, post_created_at, post_updated_at) 
       VALUES(%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, 0)"""
        cursor.execute(q, (post_pk, user_pk, post, 0, post_media_path))
        db.commit()
        toast_ok = render_template("___toast_ok.html", message="The world is reading your post !")
        tweet = {
            "post_pk": post_pk,
            "post_user_fk": user_pk,
            "user_first_name": user["user_first_name"],
            "user_last_name": user["user_last_name"],
            "user_username": user["user_username"],
            "user_avatar_path": user["user_avatar_path"],
            "post_message": post,
            "post_media_path": post_media_path,
            "post_created_at": None
        }
        html_post_container = render_template("___post_container.html")
        html_post = render_template("_tweet.html", tweet=tweet, user=user)
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
        
        # File upload errors
        if "x-error file" in str(ex):
            if "size too large" in str(ex):
                toast_error = render_template("___toast_error.html", message="Image too large. Maximum 5MB.")
            else:
                toast_error = render_template("___toast_error.html", message="Invalid file type. Only images allowed.")
            return f"""<browser mix-bottom="#toast">{toast_error}</browser>"""

        # System or developer error
        toast_error = render_template("___toast_error.html", message="System under maintenance")
        return f"""<browser mix-bottom="#toast">{ toast_error }</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

###################################
@app.route("/api-delete-post/<post_pk>", methods=["DELETE"])
def api_delete_post(post_pk):
    
    try:
        user = session.get("user", None)
        # Check if user is logged in
        if not user:
            return "invalid user", 400 ## TODO: add a HTTP requests på de andre

        db, cursor = x.db()


        # Delete post from database IF its the users post
        q = "DELETE FROM posts WHERE post_pk = %s and post_user_fk = %s"
        cursor.execute(q, (post_pk, user["user_pk"],))
        db.commit()

        toast_ok = render_template("___toast_ok.html", message="Your post has been deleted") #TODO: Translate
        
        # Remove the post from the DOM + show toast
        # return "ok"
        return f"""
            <browser mix-bottom="#toast">{toast_ok}</browser>
            <browser mix-remove="#post_container_{post_pk}"></browser>
        """, 200

    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        toast_error = render_template("___toast_error.html", message="System under maintenance")
        return f"""<browser mix-bottom="#toast">{toast_error}</browser>""", 500

    finally: 
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


############## SINGLE POST/TWEET ################
@app.get("/single-post/<post_pk>")
def view_single_post(post_pk):
    # Check if user is logged in
    try:
        user = session.get("user", None)
        if not user:
            return "invalid user", 400 ## TODO: add a HTTP requests på de andre

        db, cursor = x.db() # Question: hvorfor skal linjen være her?

        # Get likes on a post
        q = """
        SELECT 
            users.*,
            posts.*,
            CASE 
                WHEN likes.like_user_fk IS NOT NULL THEN 1
                ELSE 0
            END AS liked_by_user
        FROM posts
        JOIN users ON users.user_pk = posts.post_user_fk
        LEFT JOIN likes 
            ON likes.like_post_fk = posts.post_pk 
            AND likes.like_user_fk = %s
        WHERE posts.post_pk = %s
        """
        cursor.execute(q, (user["user_pk"], post_pk,))
        
        tweet = cursor.fetchone()

        if not tweet:
            return "Post not found", 404


        # Get comments on a post
        q = """
        SELECT
            comments.*,
            users.user_first_name,
            users.user_username,
            users.user_avatar_path
        FROM comments
        JOIN users ON users.user_pk = comments.comment_user_fk
        WHERE comments.comment_post_fk = %s
        ORDER BY comments.created_at DESC
        """

        # ORDER BY comments.created_at DESC (means: Show the newest comments first)
        
        cursor.execute(q, (post_pk,))  
        comments = cursor.fetchall()

        # Manglede at sende post_pk til templaten
        single_post_html = render_template("_single_post.html", tweet=tweet, comments=comments, post_pk=post_pk)
        return f"""<browser mix-update="main">{ single_post_html }</browser>"""

    except Exception as ex:
        
        # SYSTEM ERROR
        toast_error = render_template("___toast_error.html", message="Error") # TODO: lav en message der passer til error
        return f"""<browser mix-bottom="#toast">{toast_error}</browser>""", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/edit-post/<post_pk>")
@x.no_cache
def edit_post(post_pk):
    try:
        # Log the incoming post_pk
        print(f"DEBUG: Received post_pk: {post_pk}")
        
        # Brug session
        user = session.get("user", "")
        if not user:
            toast_error = render_template("___toast_error.html", message="You must be logged in")
            return f"""<browser mix-bottom="#toast">{toast_error}</browser>""", 401
        
        print(f"DEBUG: User logged in: {user.get('user_pk')}")
        
        # Valider post_pk (VIGTIGT for sikkerhed!)
        post_pk = x.validate_uuid4_without_dashes(post_pk)
        print(f"DEBUG: Validated post_pk: {post_pk}")
        
        # get post from db
        db, cursor = x.db()
        q = "SELECT * FROM posts WHERE post_pk = %s AND post_user_fk = %s AND post_deleted_at = 0"
        cursor.execute(q, (post_pk, user["user_pk"]))
        post = cursor.fetchone()
        
        print(f"DEBUG: Post found: {post is not None}")
        if post:
            print(f"DEBUG: Post data: {post}")
 
        if not post:
            toast_error = render_template("___toast_error.html", message="Post not found or you don't have permission")
            return f"""<browser mix-bottom="#toast">{toast_error}</browser>""", 403
        
        print("DEBUG: About to render template")
        edit_post_html = render_template("_edit_post.html", post=post)
        print(f"DEBUG: Template rendered successfully, length: {len(edit_post_html)}")
        return f'<template mix-replace="#post_container_{post_pk}">{edit_post_html}</template>'
        
    except Exception as ex:
        print(f"ERROR: Exception occurred: {type(ex).__name__}")
        print(f"ERROR: Exception message: {str(ex)}")
        import traceback
        print(f"ERROR: Full traceback:\n{traceback.format_exc()}")
        ic(ex)
        toast_error = render_template("___toast_error.html", message="Could not load post")
        return f"""<browser mix-bottom="#toast">{toast_error}</browser>""", 500
 
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

############################## 
@app.route("/api-update-post/<post_pk>", methods=["POST"])
def api_update_post(post_pk):
    try:
        # Brug session
        user = session.get("user", "")
        if not user:
            toast_error = render_template("___toast_error.html", message="You must be logged in")
            return f"""<browser mix-bottom="#toast">{toast_error}</browser>""", 401
        # Valider post_pk
        post_pk = x.validate_uuid4_without_dashes(post_pk)
        # Get and validate new post message
        post_message = request.form.get("post_message", "").strip()
        if not post_message:
            toast_error = render_template("___toast_error.html", message="Post cannot be empty")
            return f"""<browser mix-bottom="#toast">{toast_error}</browser>""", 400
        # Validate post length
        post_message = x.validate_post(post_message)
        # Update timestamp
        post_updated_at = int(time.time())
        # Update database
        db, cursor = x.db()
        q = """UPDATE posts 
               SET post_message = %s, post_updated_at = %s 
               WHERE post_pk = %s AND post_user_fk = %s AND post_deleted_at = 0"""
        cursor.execute(q, (post_message, post_updated_at, post_pk, user["user_pk"]))
        db.commit()
        # Check if update was successful
        if cursor.rowcount != 1:
            raise Exception("Could not update post", 400)
        # Fetch updated tweets
        q = """SELECT 
                users.*,
                posts.*,
                CASE WHEN likes.like_user_fk IS NOT NULL THEN 1 ELSE 0 END AS liked_by_user
            FROM posts
            JOIN users ON users.user_pk = posts.post_user_fk
            LEFT JOIN likes ON likes.like_post_fk = posts.post_pk AND likes.like_user_fk = %s
            WHERE posts.post_deleted_at = 0
            ORDER BY posts.post_updated_at DESC, RAND()
            LIMIT 5"""
        cursor.execute(q, (user["user_pk"],))
        tweets = cursor.fetchall()
        # Send success response
        toast_ok = render_template("___toast_ok.html", message="Post updated successfully!")
        home_html = render_template("_home_comp.html", tweets=tweets)
        return f"""
<browser mix-bottom="#toast">{toast_ok}</browser>
<browser mix-update="main">{home_html}</browser>
        """
    except Exception as ex:
        ic(ex)
        if "db" in locals():
            db.rollback()
        # User validation error
        if "x-error post" in str(ex):
            toast_error = render_template("___toast_error.html", 
                message=f"Post must be {x.POST_MIN_LEN} to {x.POST_MAX_LEN} characters")
            return f"""<browser mix-bottom="#toast">{toast_error}</browser>""", 400
        # System error
        toast_error = render_template("___toast_error.html", message="Could not update post")
        return f"""<browser mix-bottom="#toast">{toast_error}</browser>""", 500
 
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/api-search")
def api_search():
    try:
        # TODO: The input search_for must be validated
        search_for = request.form.get("search_for", "")
        if not search_for: return """empty search field""", 400
        part_of_query = f"%{search_for}%"
        ic(search_for)
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
        ic(reader)
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