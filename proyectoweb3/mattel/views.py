from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Receta
from .forms import ContactoForm
from django.contrib import messages
from django.http import JsonResponse
import random


def generate_recipe_name(ingredients):
    base = ingredients[:2]
    nombre_base = " ".join(base)
    opciones = [
        f"{nombre_base} al Estilo Gourmet",
        f"Delicia de {nombre_base}",
        f"{nombre_base} en Fusión Creativa",
        f"{nombre_base} Artesanal",
        f"Selección Suprema de {nombre_base}",
        f"{nombre_base} a la Cocina Moderna"
    ]
    return random.choice(opciones)


def generar_receta_profesional(ingredientes):
    if not ingredientes:
        return None

    # Elegir ingredientes aleatorios para variar cada receta
    ingredientes_random = random.sample(ingredientes, min(len(ingredientes), 4))
    ingredientes_txt = ", ".join(ingredientes_random)

    principales = ingredientes_random[:3]
    principales_txt = ", ".join(principales)

    titulo = generate_recipe_name(ingredientes_random)

    variaciones = [
        [
            f"Lava cuidadosamente los ingredientes: {ingredientes_txt}.",
            f"Corta {principales_txt} en trozos medianos.",
            f"Saltea {principales_txt} a fuego alto para activar aromas.",
            "Añade los ingredientes restantes y cocina a fuego medio.",
            "Rectifica sazón con hierbas secas.",
            "Cocina hasta obtener una consistencia suave.",
            "Sirve caliente."
        ],
        [
            f"Enjuaga los ingredientes frescos: {ingredientes_txt}.",
            f"Corta {principales_txt} finamente.",
            f"Sofríe {principales_txt} con un toque de aceite.",
            "Agrega los demás ingredientes y mezcla bien.",
            "Añade sal, ajo y pimienta al gusto.",
            "Cocina 12 minutos a fuego medio.",
            "Sirve decorado con perejil."
        ],
        [
            f"Limpia y seca los ingredientes: {ingredientes_txt}.",
            f"Machaca ligeramente {principales_txt} para intensificar sabor.",
            f"Coloca {principales_txt} en una olla caliente.",
            "Incorpora los ingredientes restantes.",
            "Usa sal, orégano y especias suaves.",
            "Cocina lentamente para un sabor profundo.",
            "Sirve tibio."
        ]
    ]

    pasos = random.choice(variaciones)

    return {
        "nombre": titulo,
        "descripcion": f"Preparación profesional basada en {principales_txt}.",
        "pasos": pasos
    }


def generar_pasos_receta_bd(receta):
    ingredientes = [i.nombre for i in receta.ingredientes.all()]
    if not ingredientes:
        return [
            "No hay ingredientes suficientes para generar pasos."
        ]

    principales = ingredientes[:3]
    ing_txt = ", ".join(ingredientes)
    princ_txt = ", ".join(principales)

    return [
        f"Lava y prepara los ingredientes seleccionados: {ing_txt}.",
        f"Pica los ingredientes principales ({princ_txt}) en trozos similares.",
        f"Calienta una sartén y saltea {princ_txt} hasta dorar ligeramente.",
        "Agrega el resto de ingredientes y mezcla suavemente.",
        "Añade sal, pimienta y especias al gusto.",
        "Cocina a fuego medio por 10–15 minutos.",
        "Sirve caliente y disfruta de esta preparación casera."
    ]


def inicio(request):
    return render(request, 'mattel/inicio.html')


def productos(request):
    if request.GET.get("reset") == "1":
        request.session.pop("ingredientes_seleccionados", None)

    categorias = ["vegetales", "frutas", "carnes", "legumbres", "cereales", "condimentos", "especias"]

    cat = request.GET.get("cat")

    if cat in categorias:
        productos_lista = Producto.objects.filter(categoria=cat)
        titulo = f"Productos de {cat.capitalize()}"
    else:
        productos_lista = Producto.objects.all()
        titulo = "Catálogo de Productos"

    return render(request, 'mattel/productos.html', {
        'productos': productos_lista,
        'titulo': titulo,
        'categorias': categorias,
        'ingredientes_seleccionados': request.session.get("ingredientes_seleccionados", [])
    })


def distribuidor(request):
    return render(request, 'mattel/distribuidor.html')


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje enviado correctamente.')
            return redirect('contacto')
        else:
            messages.error(request, 'Ocurrió un error.')
    else:
        form = ContactoForm()
    return render(request, 'mattel/contacto.html', {'form': form})


def catalogo_categoria(request, categoria):
    if request.GET.get("reset") == "1":
        if "ingredientes_seleccionados" in request.session:
            del request.session["ingredientes_seleccionados"]

    productos = Producto.objects.filter(categoria=categoria)
    return render(request, "mattel/catalogo.html", {
        "productos": productos,
        "categoria": categoria,
        'ingredientes_seleccionados': request.session.get("ingredientes_seleccionados", [])
    })


def seleccionar_ingredientes(request):
    if request.method == "POST":
        seleccionados = request.POST.getlist("ingredientes")
        if "ingredientes_seleccionados" not in request.session:
            request.session["ingredientes_seleccionados"] = []

        actuales = set(request.session["ingredientes_seleccionados"])
        actuales.update(seleccionados)

        request.session["ingredientes_seleccionados"] = list(actuales)
        return redirect(request.META.get("HTTP_REFERER", "catalogo_categoria"))

    categorias = ["carnes", "verduras", "lácteos", "frutas", "granos"]
    return render(request, "mattel/productos.html", {
        "categorias": categorias,
        'ingredientes_seleccionados': request.session.get("ingredientes_seleccionados", [])
    })


def ver_recetas(request):
    ingredientes = request.session.get("ingredientes_seleccionados", [])

    # Recetas reales filtradas
    if ingredientes:
        recetas_filtradas = Receta.objects.filter(
            ingredientes__nombre__in=ingredientes
        ).distinct()
    else:
        recetas_filtradas = Receta.objects.none()

    recetas_lista = list(recetas_filtradas)
    random.shuffle(recetas_lista)

    sugeridas = recetas_lista[:3]
    restantes = recetas_lista[3:]

    # 🔥 Generar SIEMPRE 3 recetas dinámicas únicas
    recetas_generadas = []
    if ingredientes:
        for _ in range(3):
            recetas_generadas.append(generar_receta_profesional(ingredientes))

    return render(request, "mattel/recetas_recomendadas.html", {
        "ingredientes": ingredientes,
        "sugeridas": sugeridas,
        "recetas": restantes,
        "recetas_generadas": recetas_generadas
    })


def receta_detalle(request, index):
    ingredientes = request.session.get("ingredientes_seleccionados", [])
    receta = generar_receta_profesional(ingredientes)

    return render(request, "mattel/recetas.html", {
        "ingredientes": ingredientes,
        "receta": receta
    })


def guardar_receta(request):
    if request.method == "POST":
        ingredientes = request.session.get("ingredientes_seleccionados", [])

        if ingredientes:
            receta = Receta.objects.create(nombre="Receta Generada")
            for ing in ingredientes:
                try:
                    p = Producto.objects.get(nombre=ing)
                    receta.ingredientes.add(p)
                except Producto.DoesNotExist:
                    pass

        request.session["ingredientes_seleccionados"] = []
        return redirect("ver_recetas")

    return redirect("inicio")


def recetas_recomendadas(request):
    ingredientes = request.GET.getlist("ingredientes")

    if ingredientes:
        recetas_filtradas = Receta.objects.filter(
            ingredientes__nombre__in=ingredientes
        ).distinct()
    else:
        recetas_filtradas = Receta.objects.all()

    sugeridas = recetas_filtradas[:3]
    recetas = recetas_filtradas.exclude(id__in=[r.id for r in sugeridas])

    recetas_generadas = []
    if ingredientes:
        for _ in range(3):
            recetas_generadas.append(generar_receta_profesional(ingredientes))

    return render(request, "mattel/recetas_recomendadas.html", {
        "sugeridas": sugeridas,
        "recetas": recetas,
        "ingredientes": ingredientes,
        "recetas_generadas": recetas_generadas
    })


def receta_completa(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)

    receta.pasos_lista = generar_pasos_receta_bd(receta)

    return render(request, "mattel/receta_completa.html", {"receta": receta})


def limpiar_ingredientes(request):
    if 'ingredientes_seleccionados' in request.session:
        request.session['ingredientes_seleccionados'] = []
    return redirect(request.META.get('HTTP_REFERER', '/'))

#/////////////////////////////////////////////////////////////////////

def api_recetas_generadas(request):
    """
    Endpoint que devuelve recetas generadas en formato JSON
    """
    ingredientes = request.session.get("ingredientes_seleccionados", [])
    
    if not ingredientes:
        return JsonResponse({'recetas': [], 'ingredientes': []})
    
    # Generar 3 recetas dinámicas
    recetas_generadas = []
    for _ in range(3):
        receta = generar_receta_profesional(ingredientes)
        if receta:
            recetas_generadas.append(receta)
    
    return JsonResponse({
        'recetas': recetas_generadas,
        'ingredientes': ingredientes
    })

