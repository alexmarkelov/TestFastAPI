import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from database import SessionLocal

DB_REQUEST = "SELECT * FROM public.items_parsed where items_parsed.categories = '{/brands/limon4}' LIMIT 3"

app = FastAPI()

templates = Jinja2Templates(directory="templates/")


column_names = ['id', 'seller', 'title', 'brand', 'product_description',
                'images', 'images_count', 'videos', 'video_count', 'star',
                'reviews', 'rank', 'price', 'price_old', 'categories', 'details',
                'ship_from', 'url', 'date', 'datetime', 'position', 'search_position',
                'keywords']


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_products(request: Request, db: Session = Depends(get_db)):
    db_response = db.execute(DB_REQUEST)
    if not db_response:
        raise HTTPException(status_code=404, detail="Products not found")
    out_list = [column_names, ]
    for r in db_response:
        row = []
        for number, cell in enumerate(r):
            if number == 15:
                row.append(', '.join(key + ': ' + value for key, value in cell.items()))
                continue
            row.append(cell)
        out_list.append(row)
    return templates.TemplateResponse('template.html', context={'request': request, 'result': out_list})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
