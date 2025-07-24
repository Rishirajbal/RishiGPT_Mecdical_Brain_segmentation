import streamlit as st

st.title("RishiGPT Medical Brain Segmentation API Documentation")

languages = ["Python", "JavaScript", "cURL"]
choice = st.selectbox("Choose your language:", languages)

if choice == "Python":
    st.subheader("Python Client Installation")
    st.code("$ pip install gradio_client")

    st.subheader("Python Example")
    st.code('''
from gradio_client import Client, handle_file

client = Client("rishirajbal/RishiGPT_Medical_Brain_Segmentation")
result = client.predict(
    image_input=handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
    groq_api_key="Your_API_Key",
    api_name="/predict"
)
print(result)
''', language='python')

    st.text("Accepts 2 parameters:")
    st.markdown("1. image_input: dict (Required)\n2. groq_api_key: str (Required)")

    st.text("Returns:")
    st.markdown("[0] dict: Segmented image overlay\n[1] str: Doctor's Explanation")

elif choice == "JavaScript":
    st.subheader("JavaScript Client Installation")
    st.code("$ npm i -D @gradio/client")

    st.subheader("JavaScript Example")
    st.code('''
import { Client } from "@gradio/client";

const response = await fetch("https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png");
const exampleImage = await response.blob();

const client = await Client.connect("rishirajbal/RishiGPT_Medical_Brain_Segmentation");
const result = await client.predict("/predict", {
    image_input: exampleImage,
    groq_api_key: "Your_API_Key",
});

console.log(result.data);
''', language='javascript')

    st.text("Accepts 2 parameters:")
    st.markdown("1. image_input: Blob | File | Buffer (Required)\n2. groq_api_key: string (Required)")

    st.text("Returns:")
    st.markdown("[0] string: Segmented image overlay\n[1] string: Doctor's Explanation")

elif choice == "cURL":
    st.subheader("Confirm cURL Installation")
    st.code("$ curl --version")

    st.subheader("cURL Example")
    st.code('''
curl -X POST https://rishirajbal-rishigpt-medical-brain-segmentation.hf.space/gradio_api/call/predict -s -H "Content-Type: application/json" -d '{
  "data": [
    {"path":"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png","meta":{"_type":"gradio.FileData"}},
    "Your_API_Key"
  ]
}' \
  | awk -F'"' '{ print $4}'  \
  | read EVENT_ID; curl -N https://rishirajbal-rishigpt-medical-brain-segmentation.hf.space/gradio_api/call/predict/$EVENT_ID
''', language='bash')

    st.text("Accepts 2 parameters:")
    st.markdown("1. [0]: Blob | File | Buffer (Required)\n2. [1]: string (Required)")

    st.text("Returns:")
    st.markdown("[0] string: Segmented image overlay\n[1] string: Doctor's Explanation")
