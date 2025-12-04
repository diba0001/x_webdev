const burger = document.querySelector(".burger");
const nav = document.querySelector("nav");

// ##############################
async function server(url, method, data_source_selector, function_after_fetch){
  let conn = null
  if( method.toUpperCase() == "POST" ){
    const data_source = document.querySelector(data_source_selector)
    conn = await fetch(url, {
      method: method,
      body: new FormData(data_source)
    })    
  }
  const data_from_server = await conn.text()
  if( ! conn){ console.log("error connecting to the server") }
  window[function_after_fetch](data_from_server)
}


// ##############################
function get_search_results(url, method, data_source_selector, function_after_fetch){
  const txt_search_for = document.querySelector("#txt_search_for")
  if( txt_search_for.value == ""  ){ 
    console.log("empty search"); 
    document.querySelector("#search_results").innerHTML = ""
    document.querySelector("#search_results").classList.add("d-none")
    return false 
  }
  server(url, method, data_source_selector, function_after_fetch)
}
// ##############################
function parse_search_results(data_from_server){
  // console.log(data_from_server)
  data_from_server = JSON.parse(data_from_server)
  let users = ""
  data_from_server.forEach( (user) => {
    let user_avatar_path = user.user_avatar_path ? user.user_avatar_path : "unknown.jpg"
    let html = `
        <div class="d-flex a-items-center">
            <img src="/static/images/${user_avatar_path}" class="w-8 h-8 rounded-full" alt="Profile Picture">
            <div class="w-full ml-2">
                <p class="">
                    ${user.user_first_name} ${user.user_last_name}
                    <span class="text-c-gray:+20 text-70">@${user.user_username}</span>
                </p>                
            </div>
            <button class="px-4 py-1 text-c-white bg-c-black rounded-lg">Follow</button>
        </div>`
    users += html
  })
  console.log(users)
  document.querySelector("#search_results").innerHTML = users
  document.querySelector("#search_results").classList.remove("d-none")
}




// ##############################
burger.addEventListener("click", () => {
  // toggle nav
  nav.classList.toggle("active");

  // toggle icon
  burger.classList.toggle("open");
});

// Image preview functionality for CREATE POST
document.addEventListener('DOMContentLoaded', function() {
    const mediaInput = document.getElementById('post_media_input');
    const previewArea = document.getElementById('media_preview_area');
    
    if (mediaInput) {
        mediaInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            
            // Clear previous preview
            previewArea.innerHTML = '';
            
            if (file) {
                // Check if it's an image
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        const postContainer = document.getElementById('post_container');
                        const removeText = postContainer.dataset.removeText;
                        
                        const preview = document.createElement('div');
                        preview.className = 'media-preview';
                        preview.innerHTML = `
                            <img src="${e.target.result}" alt="Preview" style="max-width: 100%; max-height: 300px; border-radius: 8px; margin: 10px 0;">
                            <button type="button" class="btn-cancel" style="margin-left: 10px;">
                                <i class="fa-solid fa-times"></i> ${removeText}
                            </button>
                        `;
                        
                        previewArea.appendChild(preview);
                        
                        // Add remove functionality
                        preview.querySelector('.btn-cancel').addEventListener('click', function() {
                            previewArea.innerHTML = '';
                            mediaInput.value = '';
                        });
                    };
                    
                    reader.readAsDataURL(file);
                }
            }
        });
    }

    // Use event delegation for dynamically loaded edit inputs
    attachEditMediaPreviewListeners();
});

// Function to attach edit media preview listeners (can be called multiple times)
function attachEditMediaPreviewListeners() {
    document.addEventListener('change', function(e) {
        // Check if the changed element is an edit media input
        if (e.target && e.target.id && e.target.id.startsWith('edit_media_input_')) {
            const postPk = e.target.id.replace('edit_media_input_', '');
            const file = e.target.files[0];
            const previewArea = document.getElementById(`new_media_preview_${postPk}`);
            
            if (!previewArea) return;
            
            previewArea.innerHTML = '';
            
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                
                reader.onload = function(event) {
                    const preview = document.createElement('div');
                    preview.className = 'media-preview';
                    preview.innerHTML = `
                        <img src="${event.target.result}" alt="Preview" style="max-width: 100%; max-height: 300px; border-radius: 8px; margin: 10px 0;">
                        <button type="button" class="remove-new-preview-btn" style="margin-left: 10px;">
                            <i class="fa-solid fa-times"></i> Remove
                        </button>
                    `;
                    previewArea.appendChild(preview);
                    
                    // Add remove functionality for new preview
                    preview.querySelector('.remove-new-preview-btn').addEventListener('click', function() {
                        previewArea.innerHTML = '';
                        document.getElementById(`edit_media_input_${postPk}`).value = '';
                    });
                };
                
                reader.readAsDataURL(file);
            }
        }
    });
}

// Remove existing media in edit mode
function removeEditMedia(postPk) {
    // Mark the media for removal FIRST (before clearing the preview)
    const removeInput = document.getElementById(`remove_media_${postPk}`);
    if (removeInput) {
        removeInput.value = '1';
        console.log(`Marked media for removal: remove_media_${postPk} = 1`);
    } else {
        console.error(`Could not find remove_media input for post ${postPk}`);
    }
    
    // Clear the preview
    const previewArea = document.getElementById(`edit_media_preview_${postPk}`);
    if (previewArea) {
        previewArea.innerHTML = '';
    }
}