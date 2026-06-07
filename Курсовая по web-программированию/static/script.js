// =======================
// Переключение страниц
// =======================

function showPage(pageId){

    document
        .querySelectorAll(".page")
        .forEach(page => {
            page.classList.remove("active");
        });

    document
        .getElementById(pageId)
        .classList.add("active");
}

// =======================
// Открытие чата
// =======================

function toggleChat(){

    const chat =
        document.getElementById("chatWindow");

    if(chat.style.display === "flex"){
        chat.style.display = "none";
    }
    else{
        chat.style.display = "flex";
    }
}

// =======================
// Отправка сообщения ИИ
// =======================

async function sendMessage(){

    const input =
        document.getElementById("messageInput");

    const text =
        input.value.trim();

    if(text === ""){
        return;
    }

    const messages =
        document.getElementById("messages");

    messages.innerHTML += `
        <div class="user">
            ${text}
        </div>
    `;

    input.value = "";

    messages.scrollTop =
        messages.scrollHeight;

    try{

        const response =
            await fetch("/api/chat", {

                method: "POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    message:text
                })

            });

        const data =
            await response.json();

        messages.innerHTML += `
            <div class="bot">
                ${data.answer}
            </div>
        `;

    }
    catch(error){

        messages.innerHTML += `
            <div class="bot">
                Ошибка подключения к серверу.
            </div>
        `;

        console.error(error);
    }

    messages.scrollTop =
        messages.scrollHeight;
}

// =======================
// Enter для отправки
// =======================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        showPage("home");

        document
        .getElementById("messageInput")
        .addEventListener("keydown", function(event){

            if(event.key === "Enter"){
                sendMessage();
            }

        });

    }
);

// =======================
// Форма записи
// =======================

document.addEventListener(
    "submit",
    function(event){

        if(
            event.target.classList.contains(
                "appointment-form"
            )
        ){

            event.preventDefault();

            alert(
                "Заявка успешно отправлена!"
            );

        }

    }
);