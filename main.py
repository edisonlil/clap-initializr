import io
import os
import zipfile
from pathlib import Path

import streamlit as st

st.set_page_config(layout="wide")
st.set_page_config.window_title = "Clap Initializer"

st.title("Clap Initializer")
st.markdown("""
----
""")

col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.markdown("### Clap Domain Version")
    domain_version = st.radio(
        "selector",
        ["1.0.0", "1.0.1", "1.0.2-SNAPSHOT"],
        index=2, horizontal=True
    )
    st.write("You selected:", domain_version)

    st.markdown("### Clap Metadata")

    group = st.text_input('Group', 'com.example')
    artifact = st.text_input('Artifact', 'demo')
    name = st.text_input('Name', 'demo')
    desc = st.text_input('Description', 'Demo project for Clap')
    pkg_name = st.text_input('Package Name', 'com.example.demo')

with col2:
    st.subheader("Dependencies")
    options = st.multiselect(
        'Dependencies',
        ['Clap-dict-domain', 'Clap-identity-domain', 'Clap-access-domain', 'Clap-bizlog-domain'],
        ['Clap-dict-domain'])

    st.write('You selected:', options)

st.markdown("---")
generate = st.button("Generate Zip", type="primary")


def iter_dir(path=str, func=None, step=1):
    from pathlib import Path
    dir = Path(path)
    for child in dir.glob("*"):
        if child.is_file():  # 检查是否为文件
            st.write(f"Found file: {child}")
            func(child)
        elif child.is_dir():  # 检查是否为目录
            st.write(f"Found directory: {child}")
            func(child)
            iter_dir(child, func)


def zipdir(path, ziph, exclude=None):
    # ziph 是 zipfile 对象
    for root, dirs, files in os.walk(path):
        for file in files:
            if exclude and os.path.splitext(file)[1][1:] in exclude:
                continue  # 跳过指定的文件类型
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


if generate:
    st.markdown("### Generating...")

    from jinja2 import Template


    def func(file=Path):

        if not os.path.exists("./gen"):
            os.mkdir("./gen")

        if file.is_file():  # 检查是否为文件

            if file.suffix == ".java":
                return


            content = file.read_text(encoding="utf-8")

            template_content = Template(content)
            content = template_content.render(
                {
                    "group": group,
                    "artifact": artifact,
                    "projectName": name,
                    "domainVersion": domain_version,
                    "domainSet": [s.lower() for s in options]
                }
            )

            # 构建二级目录
            genPath = './gen/' + name
            if str(file.parent).__contains__('clap-initializer-server'):
                genPath = './gen/' + name + '/' + name + '-server'
            elif str(file.parent).__contains__('clap-initializer-sdk'):
                genPath = './gen/' + name + '/' + name + '-sdk'

            # 生成pom.xml
            with open(genPath + "/pom.xml", "w") as pom:
                pom.write(content)

            pass
        elif file.is_dir():  # 检查是否为目录

            genPath = './gen/' + name

            if str(file).__contains__('clap-initializer-server'):
                genPath = './gen/' + name + '/' + name + '-server'
            elif str(file).__contains__('clap-initializer-sdk'):
                genPath = './gen/' + name + '/' + name + '-sdk'

            if not os.path.exists(genPath):
                os.mkdir(genPath)

            # 如果是server目录下则
            if str(file).__contains__('clap-initializer-server'):
                full_pkg_name = genPath + "/src/main/java/" + pkg_name.replace(".", "/")
                os.makedirs(full_pkg_name, exist_ok=True)
                os.makedirs(genPath + "/src/main/resources", exist_ok=True)
                os.makedirs(genPath + "/src/main/resources/mapper", exist_ok=True)

                # 生成Application.java
                with open("./template/Application.java") as f:
                    content = f.read()
                    template_content = Template(content)
                    content = template_content.render(
                        {
                            "pkgName": pkg_name
                        }
                    )
                    open(full_pkg_name + "/Application.java", "w").write(content)

                # 生成Application.java
                with open("./template/Application.java") as f:
                    content = f.read()
                    template_content = Template(content)
                    content = template_content.render(
                        {
                            "pkgName": pkg_name
                        }
                    )
                    open(full_pkg_name + "/Application.java", "w").write(content)

    iter_dir('./template', func)

    genPath = './gen/' + name
    zipPath = './gen/' + name + '.zip'
    zipf = zipfile.ZipFile(zipPath, "w", zipfile.ZIP_DEFLATED)
    zipdir(genPath, zipf)
    zipf.close()

    with open(zipPath, "rb") as f:
        zip_file_bytes = f.read()

    # 使用 io.BytesIO 创建一个字节流，并将其传递给 download_button
    st.download_button(
        label=f"Download {name}.zip",
        data=io.BytesIO(zip_file_bytes),
        file_name=f"{name}.zip",
        mime="application/zip",
    )
