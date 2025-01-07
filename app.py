import streamlit as st
from gradio_client import Client
# from gradio_client.exceptions import AppError

st.set_page_config(page_title="Image generator AI", page_icon="🎨")

client = Client("multimodalart/FLUX.1-merged")

def generate_image(prompt, seed, randomize_seed, width, height, guidance_scale, num_inference_steps):
    try:
        result = client.predict(
            prompt=prompt,
            seed=seed,
            randomize_seed=randomize_seed,
            width=width,
            height=height,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            api_name="/infer"
        )
        return result[0]
    except Exception as e:
        if "GPU quota" in str(e):
            st.error("GPU time limit reached. Please try again later")
            return None
        else:
            st.error("Wystąpił błąd: " + str(e))
            return None

# st.title("Generator obrazków")
st.markdown("[![100pa.com](https://www.100pa.com/images/logo.png)](https://100pa.com/)")
st.write("# 🖼️ 🎨 AI Image Generator") 

prompt = st.text_area("Prompt, write what you would like to see in the picture", height=70)

col1, col2, col3, col4 = st.columns(4)
seed = col1.slider("Seed", 0, 100, 0)
randomize_seed = col2.checkbox("Randomize Seed", value=True)
guidance_scale = col3.slider("Guidance Scale", 1.0, 10.0, 3.5, 0.1)
num_inference_steps = col4.slider("Number of inference steps", 1, 16, 8)

col5, col6 = st.columns(2)
width = col5.slider("Width", 512, 2048, 1024, 128)
height = col6.slider("Height", 512, 2048, 1024, 128)

if st.button("Generate image"):
    with st.spinner("Image is being generated..."):
        image = generate_image(prompt, seed, randomize_seed, width, height, guidance_scale, num_inference_steps)
        if image is not None:
            st.image(image)
