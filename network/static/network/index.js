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