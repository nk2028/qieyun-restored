import pickle
from tqdm import tqdm
from pypdf import PdfReader


reader = PdfReader('fujita.pdf')
pages = []


def visitor_body(text, cm, tm, font_dict, font_size):
    x, y = tm[-2:]
    pages[-1].append([text, x])


for page in tqdm(reader.pages[215:]):
    pages.append([])
    page.extract_text(visitor_text=visitor_body)

with open('raw.pkl', 'wb') as f:
    pickle.dump(pages, f)
