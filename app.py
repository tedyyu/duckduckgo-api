from itertools import islice

from duckduckgo_search import DDGS
from flask import Flask, request

app = Flask(__name__)


def run():
    print(request.args)
    form_data = request.args.to_dict(flat=False)
    print(form_data)
    for key, value in request.args.items():
        print(f'{key}: {value}')

    if request.method == 'POST':
        keywords = request.form['q']
        max_results = int(request.form.get('max_results', 10))
        safesearch = request.form.get('safesearch', 'on')
        region = request.form.get('region', 'us-en')
        timelimit = request.form.get('timelimit', None)
        backend = request.form.get('backend', 'api') #or lite?
    else:
        keywords = request.args.get('q')
        # 从请求参数中获取最大结果数，如果未指定，则默认为10
        max_results = int(request.args.get('max_results', 10))
        safesearch = request.args.get('safesearch', 'on')
        region = request.args.get('region', 'us-en')
        timelimit = request.args.get('timelimit', None)        
        backend = request.args.get('backend', 'api') #or lite?
    print(f'keywords: {keywords}, max_results: {max_results}, safesearch: {safesearch}, region: {region}, timelimit: {timelimit}, backend: {backend}')
    return keywords, max_results, safesearch, region, timelimit, backend

def runImages():
    keywords, max_results, safesearch, region, timelimit, backend = run()
    if request.method == 'POST':
        size = request.form.get('size', 'Large')
        color = request.form.get('color', None)
        type_image = request.form.get('type_image', None)
        layout = request.form.get('layout', None)
        license_image = request.form.get('license_image', None)
    else:
        size = request.args.get('size', 'Large')
        color = request.args.get('color', None)
        type_image = request.args.get('type_image', None)
        layout = request.args.get('layout', None)
        license_image = request.args.get('license_image', None)
    print(f'image size: {size}, color: {color}, type_image: {type_image}, layout: {layout}, license_image: {license_image}')
    return keywords, max_results, safesearch, region, timelimit, backend, size, color, type_image, layout, license_image

def runVideos():
    keywords, max_results, safesearch, region, timelimit, backend = run()
    if request.method == 'POST':
        resolution = request.form.get('resolution', 'high')
        duration = request.form.get('duration', None)
        license_videos = request.form.get('license_videos', None)
    else:
        resolution = request.args.get('resolution', 'high')
        duration = request.args.get('duration', None)
        license_videos = request.args.get('license_videos', None)
    print(f'video resolution: {resolution}, duration: {duration}, license_videos: {license_videos}')
    return keywords, max_results, safesearch, region, timelimit, backend, resolution, duration, license_videos


'''
original params in duckduckgo_search

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m, y. Defaults to None.
        backend: api, html, lite. Defaults to api.
            api - collect data from https://duckduckgo.com,
            html - collect data from https://html.duckduckgo.com,
            lite - collect data from https://lite.duckduckgo.com.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.
'''
@app.route('/search', methods=['GET', 'POST'])
async def search():
    keywords, max_results, safesearch, region, timelimit, backend = run()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.text(keywords, safesearch=safesearch, region=region, timelimit=timelimit, backend=backend)
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'results': results}

'''
original params in duckduckgo_search

    Args:
        keywords: keywords for query,
'''
@app.route('/searchAnswers', methods=['GET', 'POST'])
async def search_answers():
    keywords, max_results, _, _, _, _ = run()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.answers(keywords)
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'results': results}


'''
original params in duckduckgo_search
   
    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: Day, Week, Month, Year. Defaults to None.
        size: Small, Medium, Large, Wallpaper. Defaults to None.
        color: color, Monochrome, Red, Orange, Yellow, Green, Blue,
            Purple, Pink, Brown, Black, Gray, Teal, White. Defaults to None.
        type_image: photo, clipart, gif, transparent, line.
            Defaults to None.
        layout: Square, Tall, Wide. Defaults to None.
        license_image: any (All Creative Commons), Public (PublicDomain),
            Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
            Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
            Use Commercially). Defaults to None.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.
    
'''
@app.route('/searchImages', methods=['GET', 'POST'])
async def search_images():
    keywords, max_results, safesearch, region, timelimit, _, size, color, type_image, layout, license_image = runImages()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.images(keywords, safesearch=safesearch, region=region, timelimit=timelimit, size=size, color=color, type_image=type_image, layout=layout, license_image=license_image)
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'results': results}

'''
original params in duckduckgo_search

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m. Defaults to None.
        resolution: high, standart. Defaults to None.
        duration: short, medium, long. Defaults to None.
        license_videos: creativeCommon, youtube. Defaults to None.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.
    
'''
@app.route('/searchVideos', methods=['GET', 'POST'])
async def search_videos():
    keywords, max_results, safesearch, region, timelimit, _, resolution, duration, license_videos = runVideos()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.videos(keywords, safesearch=safesearch, region=region, timelimit=timelimit, resolution=resolution, duration=duration, license_videos=license_videos)
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'results': results}

'''
original params in duckduckgo_search

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m. Defaults to None.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.
    
'''
@app.route('/searchNews', methods=['GET', 'POST'])
async def search_news():
    keywords, max_results, safesearch, region, timelimit, _ = run()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.news(keywords, safesearch=safesearch, region=region, timelimit=timelimit)
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'results': results}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
