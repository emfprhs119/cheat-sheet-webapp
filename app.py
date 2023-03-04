import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import requests
import json
import os

st.set_page_config(
     page_title='Cheat sheet',
     layout="wide",
     initial_sidebar_state="expanded",
)

data_path = './data'

def add_file_list(page):
    json_default = {
        "meta": {
            "header":"",
            "columns": 2
        },
        "contents": []
    }
    save_obj(page,json_target = json_default)

def fetch_file_list():
    file_list = os.listdir(data_path)
    return file_list

def fetch_data_from_file(page):
    f = open(data_path+'/'+page+'.json','r')
    json_object = json.load(f)
    return json_object

def save_obj(page,json_target = None):
    if (json_target == None):
        json_target = json_object
    with open(data_path+'/'+page+'.json', 'w') as f:
        json.dump(json_target, f, indent=2)
        st.experimental_rerun()

def add_code(page, add_object):
    json_object['contents'] += add_object
    save_obj(page)

def content_insert_target(target,content):
    if 'header' in content:
        target.subheader(content['header'])
    if 'markdown' in content:
        target.markdown(content['markdown'], unsafe_allow_html=True)
    if 'code' in content:
        target.code(content['code'])

def changeUrl(values=None):
    url["target"] = st.session_state.page
    new_url = st.experimental_set_query_params(**url)
    st.experimental_set_query_params(**url)

# # Fetch the data
options = [file.replace('.json','') for file in fetch_file_list() if file.endswith(".json")]

# # Get the current URL and parse the query string
url = st.experimental_get_query_params()
page = url.get("target", options)[0]

json_object = fetch_data_from_file(page)
columns_num = json_object['meta']['columns']

def left_sidebar():
    st.sidebar.selectbox("시트 선택", options,key="page" ,on_change=changeUrl, index=options.index(page))

    with st.sidebar.expander('시트 추가'):
        with st.form("page_form",clear_on_submit=True):
            [col1,col2] = st.columns([2, 1])
            title_input = col1.text_input('시트 추가',placeholder='페이지명 입력',label_visibility="collapsed")
            if col2.form_submit_button('생성'):
                add_file_list(title_input)

def view_head_meta():
    [col1,col2] = st.columns([3, 1])
    col1.markdown(json_object['meta']['header'], unsafe_allow_html=True)
    columns_num = col2.slider('div-columns', min_value=1, max_value=5,  value=json_object['meta']['columns'],label_visibility="collapsed")
    if (json_object['meta']['columns'] != columns_num):
        json_object['meta']['columns'] = columns_num
        save_obj(page)

def view_body_sheet():
    contents = json_object['contents']
    columns_arr = st.columns(columns_num)
    for idx,content in enumerate(contents):
        column = columns_arr[int(idx%columns_num)]
        if 'title' in content:
            column.title(content['title'])
            for subContent in content['subContents']:
                content_insert_target(column,subContent)
        else:
            content_insert_target(column,content)

def view_body_mutate_options():
    with st.expander("코드 추가"):
        with st.form("code_form",clear_on_submit=True):
            title_input = st.text_input('Header',placeholder='타이틀 헤더 입력')
            content_area = st.text_area('Code',placeholder='치트시트 코드 입력')
            markdown_area = st.text_area('Markdown',placeholder='추가 정보 (markdown)')
            if st.form_submit_button('Submit'):
                submit_object = [{'header':title_input,'markdown':markdown_area, 'code':content_area}]
                add_code(page, submit_object)
                st.experimental_rerun()

    with st.expander("json raw 편집"):
        with st.form("raw_form",clear_on_submit=True):
            raw_area = st.text_area('Raw json',placeholder='Raw 입력',height=500,value=json.dumps(json_object, indent=2))
            if st.form_submit_button('Submit'):
                save_obj(page)

def content_page():
    view_head_meta()
    view_body_sheet()
    view_body_mutate_options()
    return None

def main():
    left_sidebar()
    content_page()
    return None

if __name__ == '__main__':
    main()