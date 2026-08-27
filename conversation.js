const input = document.getElementById("conversationInput");
const sendButton = document.getElementById("conversationSend");
const messages = document.getElementById("conversationMessages");
const statusText =
    document.getElementById("conversationStatusText");

function setConversationStatus(state) {
    statusText.textContent = state;
}

const BRIDGE_URL = "http://127.0.0.1:8765";

let lastEventId = 0;


function addMessage(text, sender) {
    const message = document.createElement("div");

    message.className =
        sender === "user"
            ? "message user-message"
            : "message igris-message";

    const label = document.createElement("span");

    label.className = "message-label";

    label.textContent =
        sender === "user"
            ? "YOU"
            : "I.G.R.I.S.";


    const content = document.createElement("p");

    content.textContent = text;


    message.appendChild(label);
    message.appendChild(content);

    messages.appendChild(message);

    messages.scrollTop = messages.scrollHeight;
}


async function sendMessage() {

    const text = input.value.trim();

    if (!text) {
        return;
    }
    setConversationStatus("THINKING");

    input.value = "";
    input.focus();


    try {

        const response = await fetch(
            `${BRIDGE_URL}/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: text
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "I.G.R.I.S. bridge error."
            );
        }
        setConversationStatus("SPEAKING");

        /*
         * Do NOT add the user message here.
         * The Python bridge adds it to the live event stream.
         */

    } catch (error) {

        console.error(
            "Chat bridge error:",
            error
        );

        addMessage(
            "I couldn't connect to my command system.",
            "igris"
        );
    }
}


async function pollConversation() {
    try {
        const response = await fetch(
            `${BRIDGE_URL}/events?since=${lastEventId}`,
            {
                cache: "no-store"
            }
        );

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        for (const event of data.events) {
            lastEventId = Math.max(
                lastEventId,
                event.id
            );

            if (event.role === "user") {
                addMessage(
                    event.text,
                    "user"
                );

                setConversationStatus("THINKING");

                document.documentElement.style.setProperty(
                    "--data-stream-speed",
                    "0.6s"
                );

                document.documentElement.style.setProperty(
                    "--data-stream-min",
                    "0.35"
                );

                document.documentElement.style.setProperty(
                    "--data-stream-max",
                    "3.8"
                );

                continue;
            }

            if (event.role === "igris") {
                addMessage(
                    event.text,
                    "igris"
                );

                setConversationStatus("READY");

                document.documentElement.style.setProperty(
                    "--data-stream-speed",
                    "1.8s"
                );

                document.documentElement.style.setProperty(
                    "--data-stream-min",
                    "0.35"
                );

                document.documentElement.style.setProperty(
                    "--data-stream-max",
                    "2.2"
                );

                continue;
            }
        }
    } catch (error) {
        console.debug(
            "Waiting for I.G.R.I.S. bridge..."
        );
    }
}
    

/* SEND BUTTON */

sendButton.addEventListener(
    "click",
    sendMessage
);


/* ENTER KEY */

input.addEventListener(
    "keydown",
    (event) => {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();
        }
    }
);


/* LIVE VOICE/TEXT CONVERSATION */

setInterval(
    pollConversation,
    300
);


pollConversation();
window.addEventListener("beforeunload", () => {
    navigator.sendBeacon(
        "http://127.0.0.1:8765/shutdown"
    );
});