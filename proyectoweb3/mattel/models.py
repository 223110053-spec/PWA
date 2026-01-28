from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('vegetales', 'Vegetales'),
        ('frutas', 'Frutas'),
        ('carnes', 'Carnes'),
        ('legumbres', 'Legumbres'),
        ('cereales', 'Cereales'),
        ('condimentos', 'Condimentos'),
        ('especias', 'Especias'),
    ]

    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre


class Contacto(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    mensaje = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.email}"


class Receta(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()

    # 🔥 NUEVOS CAMPOS PROFESIONALES 🔥
    tiempo = models.CharField(max_length=50, default="30 minutos")  
    dificultad = models.CharField(
        max_length=20,
        choices=[
            ("Fácil", "Fácil"),
            ("Media", "Media"),
            ("Difícil", "Difícil"),
        ],
        default="Fácil"
    )
    pasos = models.TextField(
        help_text="Escribe cada paso en una nueva línea.",
        default="1. Preparar ingredientes\n2. Mezclar\n3. Cocinar"
    )

    ingredientes = models.ManyToManyField(Producto, related_name='recetas')
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True)

    # 🔥 NUEVO CAMPO PARA CLASIFICAR RECETAS 🔥
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("ensalada", "Ensalada"),
            ("guisado", "Guisado"),
            ("sopa", "Sopa"),
            ("postre", "Postre"),
            ("bebida", "Bebida"),
            ("sandwich", "Sandwich"),
            ("pasta", "Pasta"),
            ("carne", "Carne"),
            ("mariscos", "Mariscos"),
            ("vegana", "Vegana"),
            ("pizza", "Pizza"),
            ("tacos", "Tacos"),
            ("wrap", "Wrap"),
            ("arroz", "Arroz"),
            ("cereal", "Cereal"),
            ("pan", "Pan"),
            ("dulce", "Dulce"),
            ("salado", "Salado"),
            ("light", "Light"),
            ("rápida", "Rápida"),
        ],
        default="ensalada"
    )

    def pasos_lista(self):
        return self.pasos.split("\n")

    def __str__(self):
        return self.nombre