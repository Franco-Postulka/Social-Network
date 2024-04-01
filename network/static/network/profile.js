document.addEventListener('DOMContentLoaded',function(){
    const  buttom = document.querySelector('#follow_buttom')
    const logged_user = document.querySelector('#hidden-element').innerHTML
    let username = document.querySelector('#username').innerHTML
    username = username.slice(1,username.length)

    console.log(`Usuario del perfil: ${username}`)
    console.log(`Usuario loggeado: ${logged_user}`)

    if (logged_user === username) {
        buttom.style.display = 'none';  
    }
    else if (logged_user === 'AnonymousUser'){
        buttom.innerHTML = 'Follow'
    }
    else {
        fetch(`/follow?logged_user=${logged_user}&user_profile=${username}`)
        .then(response => response.json())
        .then(result =>{
            if (result.message === true){
                buttom.innerHTML = 'Unfollow'
            }else if(result.message === false){
                buttom.innerHTML = 'Follow';
            }e
        })
    }

    let follow_state; 
    let followers = document.querySelector('#followers').innerHTML;
    buttom.onclick = function(){
        if (logged_user === 'AnonymousUser'){
            window.location.href = '/login';
        }
        else if (buttom.innerHTML === 'Unfollow'){
            follow_state = false;
            buttom.innerHTML = 'Follow'
            followers --;
        }else if (buttom.innerHTML === 'Follow'){
            follow_state = true;
            buttom.innerHTML = 'Unfollow'
            followers ++;
        }
        document.querySelector('#followers').innerHTML =followers;
        fetch('/change_follow',{
            method: 'PUT',
            body: JSON.stringify({
                'follow_state':follow_state,
                'logged_user':logged_user,
                'user_profile':username
            })
        })
        // .then(response =>{
        //     if(response.state === false){
        //         buttom.innerHTML === 'Follow'
        //     }else if(response.state === true){
        //         buttom.innerHTML === 'Unfollow'
        //     }
        // })
    }
})
