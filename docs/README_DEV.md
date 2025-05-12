### **Resumen técnico integral del proyecto “Don Quijote GB” (hasta el punto actual)**

---

## 1 · **Stack & entorno**

| Capa              | Herramientas                                                           |
| ----------------- | ---------------------------------------------------------------------- |
| **Back‑end**      | Python 3.11, Django 5.0.4, Django REST Framework                       |
| **Base de datos** | PostgreSQL (contenedor `db`)                                           |
| **Front‑end**     | Bootstrap 5, JS ES6 (sin frameworks)                                   |
| **Infra**         | Docker + docker‑compose                                                |
| **Otros**         | Pillow (imágenes), qrcode (tickets efectivo), whitenoise (static prod) |

```
donquijote_gb/
├─ config/           # settings, wsgi, ASGI, urls
│   └─ settings/
│       ├─ base.py   # común
│       ├─ dev.py    # DEBUG=True
│       └─ prod.py
├─ catalog/          # libros
├─ orders/           # carrito, pedidos, préstamos
├─ favorites/
├─ reviews/
├─ accounts/         # CustomUser
├─ templates/
│   ├─ base.html
│   ├─ books/
│   │   ├─ list.html
│   │   ├─ promos.html
│   │   └─ novedades.html
│   ├─ cart/
│   │   ├─ detail.html
│   │   ├─ checkout.html
│   │   ├─ checkout_success.html
│   │   └─ history.html
│   ├─ favorites/list.html
│   └─ partials/
│       ├─ book_card.html
│       └─ pagination.html
├─ static/
│   ├─ css/custom.css
│   ├─ img/ (logo.png, no-cover.png …)
│   └─ js/
│       ├─ cart_fav_dropdown.js
│       ├─ cart_list.js
│       └─ favorites_list.js
├─ docker-compose.yml
└─ Dockerfile
```

### 1.1 docker‑compose (resumen)

```yaml
services:
  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    env_file: .env
    volumes: [., staticfiles:/app/staticfiles]
    depends_on: [db]
  db:
    image: postgres:16
    environment: {POSTGRES_DB: donquijote, POSTGRES_USER: app, POSTGRES_PASSWORD: secret}
volumes: {staticfiles:}
```

---

## 2 · **Modelos clave**

```python
# catalog.models.Book
class Book(models.Model):
    TYPE_CHOICES = [("PHYS","Físico"),("EBOOK","eBook"),("AUDIO","Audiolibro")]
    title       = models.CharField(max_length=200)
    author      = models.CharField(max_length=120)
    genre       = models.CharField(max_length=3)  # FIL, NOV …
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    cover       = models.ImageField(upload_to="covers/", blank=True)
    stock       = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    # …

# favorites.models.Favorite (user <-> book unique)

# orders.models
class CartItem(models.Model):
    user, book, quantity (unique_together user+book)

class Branch(models.Model):
    name, address, google_maps_embed, is_active

class Order(models.Model):
    PAYMENT_CARD = "CARD" ; PAYMENT_CASH = "CASH"
    PAYMENT_CHOICES = [(PAYMENT_CARD,"Tarjeta"),(PAYMENT_CASH,"Efectivo 24h")]
    STATUS_PENDING="PEND" ; STATUS_PAID="PAID" ; STATUS_EXPIRED="EXP"
    user, branch(FK), payment_method, payment_status, created_at,
    expires_at(auto +24 h si efectivo), total, ticket_pdf

class OrderItem(models.Model):
    order(FK), book, quantity, price_at_purchase
    @property subtotal = quantity*price_at_purchase
```

*Pedidos* y *préstamos* comparten tabla `Order`; diferenciamos por `payment_method`.
Para **préstamo** se usa `PAYMENT_CASH` y `total=0`; en el checkout el usuario selecciona *“Préstamo (recogida en sala)”*.

---

## 3 · **Serializers & API REST** (prefijo `/api/v1/…`)

* `BookViewSet`, `CartItemViewSet`, `FavoriteViewSet`, `OrderViewSet`, `ReviewViewSet`
* Serializers enlazan libros embebidos y exponen `count` paginator.

---

## 4 · **Vistas / flujos**

| URL                            | Vista (clase/función)                         | Descripción        |
| ------------------------------ | --------------------------------------------- | ------------------ |
| `/books/`                      | `BookListView(FilterView)`                    | filtro+pag 20 pág. |
| `/books/promociones/`          | queryset `Book.objects.filter(is_promo=True)` |                    |
| `/books/novedades/`            | últimos 14 días                               |                    |
| `/cart/`                       | `cart_view`                                   | lista editable     |
| `/cart/checkout/`              | `checkout_view` + **`CheckoutForm`**          |                    |
| `/cart/checkout/success/<pk>/` | `checkout_success_view`                       |                    |
| `/cart/history/`               | pedidos del usuario                           |                    |
| `/favorites/`                  | `FavoritesListView`                           |                    |

### 4.1 CheckoutForm (campos)

* `payment_method` `choices=Order.PAYMENT_CHOICES`
* `branch` queryset `Branch.objects.filter(is_active=True)`
* `card_number`, `card_holder`, `card_expiry`, `card_cvv` (*required* sólo si método=tarjeta)

`clean()` valida stock y método.
`save(user)` crea `Order`, sus `OrderItem`, descuenta stock y elimina `CartItem`.

### 4.2 Generar ticket pago en efectivo

```python
def generate_cash_ticket(order: Order) -> BytesIO:
    qr = qrcode.make(f"ORD-{order.pk}")
    pdf = FPDF(); pdf.add_page()
    pdf.image(qr.get_image(), x=10,y=10,w=40)
    pdf.set_xy(10,60); pdf.multi_cell(0,10,f"Total: ${order.total}")
    # …
    buf = io.BytesIO(pdf.output(dest='S').encode('latin-1'))
    return buf
```

`order.ticket_pdf.save(f"ticket_{order.pk}.pdf", File(buf))`

---

## 5 · **Templates & JS**

### 5.1 Navbar (en `base.html`)

```html
<a href="{% url 'catalog:book-list' %}">Catálogo</a>
<a href="{% url 'catalog:book-promos' %}">Promociones</a>
<a href="{% url 'catalog:book-novedades' %}">Novedades</a>

<input id="live-search"> <ul id="search-suggestions"></ul>
<i id="cartDropdown" data-bs-toggle="dropdown">🛒 <span id="cart-count"></span></i>
<i id="favDropdown"  data-bs-toggle="dropdown">❤️ <span id="fav-count"></span></i>
```

### 5.2 `static/js/cart_fav_dropdown.js`

* Reutilizable `loadDropdown(url, containerId, renderItem, emptyMsg, fullUrl)`
* Agrega **scroll** y máx‑alto `max-height: 60vh; overflow-y:auto;`

### 5.3 `cart/detail.html`

* Tabla editable (`.quantity-input`, `.btn-remove-item`)
* Usa filtro `mul` (añadido en `templatetags/math_extras.py`)
* Botón **Confirmar pedido** → `/cart/checkout/`

### 5.4 `cart/checkout.html`

* Paso 1 : resumen items (usa `{% for i in items %}`)
* Paso 2 : formulario `<select name="payment_method">`
* Para método tarjeta muestra campos extra con JS
* `<select name="branch">` + `<iframe id="map-iframe">` que cambia `src` vía JS:

```js
const map = document.getElementById("map-iframe");
branchSelect.addEventListener("change", e=>{
  map.src = e.target.selectedOptions[0].dataset.map;
});
```

---

## 6 · **Colores & estilo**

* Base: **Bootstrap 5** claro
* Primario: `#0066cc` (links, botones)
* Secundario: `#f5f5f5` (fondos)
* Danger: `#dc3545` (trash / quitar)
* Tipografía: `Inter`, tamaños `fs-5`, `fs-6` en cards.
* Cards libros con sombra `shadow-sm`, bordes `rounded-3`.

---

## 7 · **Comandos de operación**

```bash
# crear entorno
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# qrcode y reportlab (pdf) si no están
pip install qrcode[pil] fpdf

# docker
docker-compose up --build

# migraciones
python manage.py makemigrations
python manage.py migrate

# carga de libros demo
python manage.py loaddata sample_books.json

# crear superusuario
python manage.py createsuperuser
```

---

## 8 · **Qué falta / próximos pasos**

1. **Permitir usuario distinguir “Préstamo” (total 0) vs “Compra pagada”**

   * Botón radio adicional en CheckoutForm.
2. **Cron diaria (management command) para `Order.mark_expired()`**

   * Registrar en `crontab` o Celery beat.
3. **Panel admin**

   * Inline `OrderItem`, filtro `payment_status`.
4. **Tests** (pytest‑django) para checkout y expiración.
5. **CI** : GitHub Actions ⇒ `docker-compose run web python -m pytest`.

---

## 9 · **Requisitos del proyecto (resumen original)**

* Catálogo de ≥ 50 libros con filtros, buscador vivo y paginación.
* Carrito y favoritos en dropdown con contador dinámico.
* Pedido/préstamo con selección de sucursal y simulación de pago (tarjeta/efectivo).
* Ticket QR + PDF para efectivo (24 h).
* Historial pedidos & préstamos.
* Reseñas y calificaciones (estrella).
* Promociones (flag `is_promo=True`) y Novedades (≤ 14 días).
* Responsive, colores accesibles AA.

---
