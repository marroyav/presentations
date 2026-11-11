"""Render draw.io SVG exports as vector PDFs for the Beamer deck."""
import asyncio, re, xml.etree.ElementTree as ET
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent
BROWSER=Path('/home/arroyave/.cache/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-linux64/chrome-headless-shell')
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path=str(BROWSER),args=['--no-sandbox'])
  page=await browser.new_page(device_scale_factor=2)
  for name in ['overview','daphne','pof','lasers','racks']:
   svg=(ROOT/f'{name}.drawio.svg').read_text()
   dims=ET.fromstring(svg).attrib
   w=float(re.sub('[^0-9.]','',dims['width']));h=float(re.sub('[^0-9.]','',dims['height']))
   # Keep HTML labels; omit fallback text that can be painted twice in exports.
   def label(m):
    content=m.group(1)
    foreign=re.search(r'<foreignObject\b.*?</foreignObject>',content,re.S)
    return foreign.group(0) if foreign else ''
   svg=re.sub(r'<switch>(.*?)</switch>',label,svg,flags=re.S)
   html=f'<html><head><style>@page{{size:{w}px {h}px;margin:0}}html,body{{margin:0;width:{w}px;height:{h}px;background:#101820;}}svg{{display:block}}*{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}</style></head><body>{svg}</body></html>'
   await page.set_viewport_size({'width':int(w+1),'height':int(h+1)})
   await page.set_content(html,wait_until='load')
   await page.emulate_media(media='print',color_scheme='light')
   await page.pdf(path=str(ROOT.parent/'figures'/f'drawio-{name}.pdf'),width=f'{w}px',height=f'{h}px',margin={'top':'0','left':'0','bottom':'0','right':'0'},print_background=True)
   await page.screenshot(path=f'/tmp/dps-drawio-{name}.png',full_page=True)
   print(name,round(w),round(h))
  await browser.close()
asyncio.run(main())
