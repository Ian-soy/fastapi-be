import os
from leptonai.client import Client
from components.spb import storage_client

def generate_image(prompt, uuid, timestamp):

    api_token = os.getenv("LEPTON_API_KEY")
    c = Client("https://sdxl.lepton.run", token=api_token)
    image = c.run(
        # prompt="An anime girl who are playing basketball during a sunset",
        prompt=prompt,
        height=1024,
        width=1024,
        guidance_scale=5,
        high_noise_frac=0.75,
        seed=1809774958,
        steps=30,
        use_refiner=False
    )
    with open(uuid + '.png', 'wb') as f:
        f.write(image)
    print("Image saved as output_image.png")
    
    # 读取 MP3 文件内容
    with open(uuid + '.png', 'rb') as file:
      mp3_content = file.read()

    bucket_name = 'resource-online'
    file_name = "file/" + timestamp + '/' + uuid + '.png'

    response = storage_client().from_(bucket_name).upload(file_name, mp3_content, {
      'content-type': 'image/png',
    })
    
    # 上传完成之后删除本地文件
    os.remove(uuid + '.png')
    
    return file_name