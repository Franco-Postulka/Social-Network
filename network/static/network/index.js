function edit(post_pk) {
    const button = document.getElementById(`${post_pk}`)
    const paragraph = document.getElementById(`Paragraph${post_pk}`);
    const textarea = document.getElementById(`Textarea${post_pk}`);

    if (button.innerHTML === 'Edit'){

        button.innerHTML = 'Save';

        textarea.value= paragraph.innerHTML;

        paragraph.style.display = 'none';
        textarea.style.display = 'block';

    }else if(button.innerHTML === 'Save'){
        fetch('/edit',{
            method:'PUT',
            body:JSON.stringify({
                paragraph:textarea.value,
                post_id:post_pk,
            })
        })
        .then(response =>response.json())
        .then(result => {
            if (result.error){
                console.log(result.error)
            }else if(result.edited){
                paragraph.innerHTML = textarea.value;
                button.innerHTML = 'Edit';
                paragraph.style.display = 'block';
                textarea.style.display = 'none';
            }
        })
    }
}

function like(post_pk, like_or_unlike){
    const like_button = document.getElementById(`like_post${post_pk}`)
    const unlike_button = document.getElementById(`unlike_post${post_pk}`)
    let likes = parseInt(like_button.querySelector('span').innerHTML)
    const logged_user = document.getElementById('hidden-element').innerHTML

    if (logged_user === 'AnonymousUser'){
        window.location.href = '/login';
    }else if (like_or_unlike === 'like'){
        fetch('/like',{
            method:'PUT',
            body: JSON.stringify({
                post_id:post_pk,
                like_or_unlike:like_or_unlike,
            })
        })
        .then(response => response.json())
        .then(result =>{
            if (result.success){
                likes ++;
        
                unlike_button.querySelector('span').innerHTML = likes
                like_button.querySelector('span').innerHTML = likes
        
                like_button.style.display = 'none';
                unlike_button.style.display= 'block';
            }
        })

    }else if (like_or_unlike === 'unlike'){
        fetch('/like',{
            method:'PUT',
            body: JSON.stringify({
                post_id:post_pk,
                like_or_unlike:like_or_unlike,
            })
        })
        .then(response => response.json())
        .then(result =>{
            if (result.success){
                likes --;
        
                like_button.querySelector('span').innerHTML = likes
                unlike_button.querySelector('span').innerHTML = likes
        
                unlike_button.style.display= 'none';
                like_button.style.display = 'block';
            }
        })
    }
}

