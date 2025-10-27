from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_recipes_by_ingredient(ingredient):
    url = f'https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient.strip()}'
    response = requests.get(url)
    data = response.json()
    if data['meals']:
        return set((m['idMeal'], m['strMeal'], m['strMealThumb']) for m in data['meals'])
    return set()

@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = set()
    error = None
    if request.method == 'POST':
        ingredient_input = request.form.get('ingredient')
        ingredients = [i.strip() for i in ingredient_input.split(',') if i.strip()]
        if not ingredients:
            error = 'Please enter one or more ingredients.'
        else:
            recipe_sets = [get_recipes_by_ingredient(i) for i in ingredients]
            if recipe_sets and all(recipe_sets):  
                recipes = set.intersection(*recipe_sets)
                if not recipes:
                    error = 'No recipes found with all those ingredients!'
            else:
                error = 'No recipes found for one or more ingredients!'
    return render_template('index.html', recipes=recipes, error=error)

@app.route('/recipe/<id>')
def recipe_detail(id):
    url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}'
    response = requests.get(url)
    data = response.json()
    recipe = data['meals'][0] if data['meals'] else None
    return render_template('results.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)
