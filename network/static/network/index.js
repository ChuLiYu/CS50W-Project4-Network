document.addEventListener('DOMContentLoaded', function () {

  const likeLinks = document.querySelectorAll('.like-link');
  const editLinks = document.querySelectorAll('.edit-post-link')
  const csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
  const followLinks = document.querySelectorAll('.follow-link')

  followLinks.forEach(link => {
    link.onclick = () => {
      try {
        var like_author = document.querySelector('#username').innerHTML;

      } catch (TypeError) {
        alert('Please log in.')
        return false
      }
    }
  })



  likeLinks.forEach(link => {
    link.onclick = (event) => {
      const cardBody = event.target.parentElement;

      try {
        var like_author = document.querySelector('#username').innerHTML;

      } catch (TypeError) {
        alert('Please log in.')
        return false
      }

      const data = {
        like_author: like_author,
        liked_post: cardBody.dataset.post_id
      }

      fetch('/like', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
      })
        .then(response => response.json())
        .then(data => {
          event.target.innerHTML = data.likes;
          if (link.style.color === "") { link.style.color = "rgb(247, 120, 107" } else {
            link.style.color = ""
          }
        })
        .catch(error => console.error(error));
    }
  })

  editLinks.forEach((link) => {
    link.onclick = () => {
      link.style.display = "none"

      let editForm = link.parentElement.querySelector("[name='edit_form']")
      let originalTextDiv = link.parentElement.querySelector("[name='text-content']")

      originalTextDiv.classList.add('d-none')
      editForm.classList.remove('d-none')

      editForm.querySelector("[name='text-content']").value = originalTextDiv.innerHTML


    }
  })





})