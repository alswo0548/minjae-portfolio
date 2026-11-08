from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

W,H=1672,941
OUT=Path('assets/portfolio-covers')
OUT.mkdir(parents=True,exist_ok=True)
FONT_REG='/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
FONT_BOLD='/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf'

def font(size,bold=False):
    path=FONT_BOLD if bold else FONT_REG
    return ImageFont.truetype(path,size)

def bg(accent):
    canvas=Image.new('RGB',(W,H),'#0b1223')
    d=ImageDraw.Draw(canvas)
    for y in range(H):
        t=y/H
        d.line((0,y,W,y),fill=(int(11+6*t),int(18+6*t),int(35+17*t)))
    glow=Image.new('RGBA',(W,H),(0,0,0,0))
    ImageDraw.Draw(glow).ellipse((1000,-140,1940,960),fill=(*accent,48))
    return Image.alpha_composite(canvas.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(140)))

def rounded_screen(im,path,box,radius=20,frame=11):
    x,y,w,h=box
    photo=Image.open(path).convert('RGB')
    iw,ih=w-2*frame,h-2*frame
    tile=Image.new('RGB',(iw,ih),'#101827')
    fit=ImageOps.contain(photo,(iw,ih),Image.Resampling.LANCZOS)
    tile.paste(fit,((iw-fit.width)//2,(ih-fit.height)//2))
    shell=Image.new('RGBA',(w,h),(0,0,0,0))
    ImageDraw.Draw(shell).rounded_rectangle((0,0,w-1,h-1),radius=radius,fill=(33,47,68,255),outline=(95,119,147,250),width=3)
    mask=Image.new('L',(iw,ih))
    ImageDraw.Draw(mask).rounded_rectangle((0,0,iw-1,ih-1),radius=max(3,radius-frame),fill=255)
    shell.paste(tile,(frame,frame),mask)
    shadow=Image.new('RGBA',(w+70,h+75),(0,0,0,0))
    shadow.alpha_composite(shell,(30,19))
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(29)),(x-30,y-19))
    im.alpha_composite(shell,(x,y))

def cover(key,index,title,subtitle,description,tags,accent,kind,paths):
    im=bg(accent)
    d=ImageDraw.Draw(im)
    left=86
    label='SOLO PROJECT' if kind=='web' else 'TEAM PROJECT'
    d.text((left,121),f'{index} · {label}',font=font(30,True),fill=(*accent,255))
    d.text((left,212),title,font=font(104 if len(title)<10 else 77,True),fill='white')
    d.text((left,364),subtitle,font=font(45 if len(subtitle)<18 else 38,True),fill='white')
    y=462
    for line in description:
        d.text((left,y),line,font=font(27),fill=(198,209,225,255))
        y+=43
    tx,ty=left,615
    for tag in tags:
        tw=d.textbbox((0,0),tag,font=font(25,True))[2]
        width=tw+44
        if tx+width>810:
            tx=left
            ty+=76
        d.rounded_rectangle((tx,ty,tx+width,ty+55),radius=27,outline=(*accent,255),width=3,fill=(16,25,41,235))
        d.text((tx+22,ty+7),tag,font=font(25,True),fill=(245,248,255,255))
        tx+=width+15
    if kind=='octv':
        rounded_screen(im,paths[0],(809,200,720,510),radius=25,frame=14)
        rounded_screen(im,paths[1],(1390,377,208,445),radius=28,frame=12)
        d.text((1290,117),'DISASTER RESPONSE',font=font(26),fill=(214,229,250,255))
        d.rounded_rectangle((1237,130,1272,135),radius=2,fill=(*accent,255))
    elif kind=='gdq':
        rounded_screen(im,paths[0],(885,182,325,632),radius=43,frame=16)
        rounded_screen(im,paths[1],(1190,230,329,620),radius=43,frame=16)
        d.text((1360,116),'SOCIAL GOOD',font=font(27),fill=(216,237,229,255))
    else:
        rounded_screen(im,paths[0],(817,207,751,525),radius=24,frame=15)
        rounded_screen(im,paths[1],(790,574,352,216),radius=17,frame=10)
        d.text((1280,119),'CLIMBING & DATA',font=font(26),fill=(248,225,208,255))
    out=OUT/f'{key}.webp'
    im.convert('RGB').save(out,'WEBP',quality=86,method=6)
    print(out,out.stat().st_size)

cover('octv','01','OCTV','AI 재난 대응 출동 지원 플랫폼',
      ['CCTV 탐지 이후의 위험도 판단과','기관·경로 추천, 상황실 전달'],
      ['Python','FastAPI','LangGraph','Redis','Celery'],(97,151,234),'octv',
      ['assets/01-octv/screens/overview.jpg','assets/01-octv/mobile-incident.jpg'])
cover('gooddeedquest','02','GoodDeedQuest','AI 기반 선행 퀘스트 플랫폼',
      ['개인화 커뮤니티와 팀 챌린지','AI 추천 및 관리자 기능 구현'],
      ['FastAPI','PostgreSQL','LangGraph','GPT-4o','React Native'],(103,222,164),'gdq',
      ['assets/02-gooddeedquest/01_community_algorithm.jpg','assets/02-gooddeedquest/02_team_challenge_llm.jpg'])
cover('climbing','03','Climbing Web','클라이밍장 정보 · 추천 · 기록',
      ['지도 검색과 성향 기반 추천','선수 기록 및 데이터 시각화'],
      ['HTML','CSS','JavaScript','Kakao Maps','Chart.js'],(255,146,60),'web',
      ['assets/03-climbing-web/screens/main.jpg','assets/03-climbing-web/01_gym_map_search.jpg'])
