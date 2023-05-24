import torch
import streamlit as st
import uuid
import os

from model import ResNet
from torchvision import transforms
from PIL import Image


st.set_page_config(
    page_title="Channa Classification",
    page_icon="logo/favicon.ico",
)

torch.manual_seed(128)
# Define the class names
class_names = ['Andrao', 'Asiatica', 'Auranti', 'Barca', 'Maru', 'Stewartii']

# Define the transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load the model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
state_dict = torch.load('ResNetv1.pt', map_location=device)
model = ResNet()
model.load_state_dict(state_dict)
model = model.to(device)

# Create the predict function
def predict(image):
    image = transform(image).unsqueeze(0)
    output = model(image)
    _, predicted_idx = torch.max(output, 1)
    predicted_label = class_names[predicted_idx.item()]
    return predicted_label

# Function to save the image, prediction results, and accuracy
def save_result(image, predicted_label):
    unique_filename = f"hasil/{uuid.uuid4().hex[:10]}"
    save_image(image, f"{unique_filename}.jpg")
    save_prediction(predicted_label, f"{unique_filename}.txt")

# Function to save the image
def save_image(image, filename):
    image.save(filename)

# Function to save the prediction result to a file
def save_prediction(predicted_label, filename):
    with open(filename, "w") as f:
        f.write(f"\n{predicted_label}")

# Function to display the image and prediction
def show_prediction(predicted_label):
    st.info(f"Hasil prediksi: {predicted_label}")

def stewartii_recomendation(predicted_label):
    col1, col2, col3 = st.columns([3,3,3])
    with col1:
        st.button("Kunjungi Tokopedia")
        st.markdown("<a href='https://www.tokopedia.com/zengaquaticbandung/ikan-channa-auranti-chana-auranti-grade-a-size-25-30-cm-spek-kontes?extParam=ivf%3Dtrue&src=topads' target='_blank'>Klik di sini</a> untuk mengunjungi Tokopedia.", unsafe_allow_html=True)
    with col2: 
        st.button("Kunjungi Shopee")
        st.markdown("<a href='https://www.tokopedia.com/zengaquaticbandung/ikan-channa-auranti-chana-auranti-grade-a-size-25-30-cm-spek-kontes?extParam=ivf%3Dtrue&src=topads' target='_blank'>Klik di sini</a> untuk mengunjungi Tokopedia.", unsafe_allow_html=True)
    with col3:
        st.button("Kunjungi Lazada")
        st.markdown("<a href='https://www.tokopedia.com/zengaquaticbandung/ikan-channa-auranti-chana-auranti-grade-a-size-25-30-cm-spek-kontes?extParam=ivf%3Dtrue&src=topads' target='_blank'>Klik di sini</a> untuk mengunjungi Tokopedia.", unsafe_allow_html=True)

# Create the Streamlit app
def main():
    st.title("Channa Classifier")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        resized_image = Image.open(uploaded_image)
        image = resized_image.resize((250, 100))  # Atur ukuran gambar menggunakan transformasi PIL
        st.image(image, caption="Uploaded Image", use_column_width=True)  # Tampilkan gambar yang diunggah dengan lebar kolom konten
        if st.button("Predict"):
            # Perform image prediction
            predicted_label = predict(image)
            show_prediction(predicted_label)
            st.success(f"Prediksi Berhasil!")
            save_result(image, predicted_label)
            if predicted_label == "Stewartii":
                st.markdown(
                    """
                    <p style='text-align: center; color: #FF0000;'>Rekomendasi Toko</p>
                    """
                    , unsafe_allow_html=True
                )
                stewartii_recomendation(predicted_label)
                

# Create the "hasil" folder if it doesn't exist
if not os.path.exists("hasil"):
    os.makedirs("hasil")

# Run the main application
if __name__ == "__main__":
    main()