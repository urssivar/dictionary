#!/usr/bin/env python3
"""Suggest semantic tags for entries based on translations."""

import yaml
from pathlib import Path
from collections import defaultdict

# Keyword patterns for tag suggestions
TAG_PATTERNS = {
    'animal': [
        'animal', 'beast', 'creature', 'mammal', 'livestock', 'cattle', 'horse', 'cow',
        'sheep', 'goat', 'dog', 'cat', 'wolf', 'fox', 'bear', 'rabbit', 'mouse', 'rat',
        'животное', 'зверь', 'скот', 'корова', 'лошадь', 'овца', 'коза', 'собака',
        'кошка', 'волк', 'лиса', 'медведь', 'заяц', 'мышь', 'крыса',
    ],
    'bird': [
        'bird', 'chicken', 'rooster', 'hen', 'duck', 'goose', 'turkey', 'eagle', 'hawk',
        'crow', 'raven', 'sparrow', 'pigeon', 'dove', 'owl', 'swallow', 'stork',
        'птица', 'курица', 'петух', 'утка', 'гусь', 'индюк', 'орёл', 'ястреб',
        'ворон', 'воробей', 'голубь', 'сова', 'ласточка', 'аист',
    ],
    'insect': [
        'insect', 'bug', 'fly', 'mosquito', 'bee', 'wasp', 'ant', 'spider', 'beetle',
        'butterfly', 'moth', 'flea', 'louse', 'tick',
        'насекомое', 'муха', 'комар', 'пчела', 'оса', 'муравей', 'паук', 'жук',
        'бабочка', 'моль', 'блоха', 'вошь', 'клещ',
    ],
    'fish': [
        'fish', 'salmon', 'trout', 'carp', 'pike', 'sturgeon',
        'рыба', 'лосось', 'форель', 'карп', 'щука', 'осётр',
    ],
    'plant': [
        'plant', 'weed', 'herb', 'vegetation', 'flora',
        'растение', 'трава', 'сорняк', 'зелень', 'флора',
    ],
    'tree': [
        'tree', 'oak', 'pine', 'birch', 'willow', 'maple', 'poplar', 'elm', 'cedar',
        'дерево', 'дуб', 'сосна', 'берёза', 'ива', 'клён', 'тополь', 'вяз', 'кедр',
    ],
    'bush': [
        'bush', 'shrub', 'bramble', 'thicket',
        'куст', 'кустарник', 'заросль',
    ],
    'flower': [
        'flower', 'blossom', 'bloom', 'rose', 'tulip', 'lily',
        'цветок', 'роза', 'тюльпан', 'лилия',
    ],
    'fruit': [
        'apple', 'pear', 'plum', 'cherry', 'peach', 'apricot', 'grape', 'melon',
        'watermelon', 'orange', 'lemon',
        'яблоко', 'груша', 'слива', 'вишня', 'персик', 'абрикос', 'виноград',
        'дыня', 'арбуз', 'апельсин', 'лимон',
    ],
    'berry': [
        'berry', 'strawberry', 'raspberry', 'blackberry', 'blueberry', 'currant',
        'ягода', 'клубника', 'малина', 'ежевика', 'черника', 'смородина',
    ],
    'grass': [
        'grass', 'hay', 'straw', 'lawn', 'meadow',
        'трава', 'сено', 'солома', 'газон', 'луг',
    ],
    'body': [
        'head', 'eye', 'ear', 'nose', 'mouth', 'tooth', 'tongue', 'neck', 'shoulder',
        'arm', 'hand', 'finger', 'leg', 'foot', 'toe', 'back', 'chest', 'stomach',
        'heart', 'liver', 'kidney', 'bone', 'skin', 'hair', 'blood', 'face',
        'голова', 'глаз', 'ухо', 'нос', 'рот', 'зуб', 'язык', 'шея', 'плечо',
        'рука', 'палец', 'нога', 'спина', 'грудь', 'живот', 'сердце', 'печень',
        'почка', 'кость', 'кожа', 'волосы', 'кровь', 'лицо',
    ],
    'kinship': [
        'mother', 'father', 'parent', 'son', 'daughter', 'child', 'brother', 'sister',
        'grandfather', 'grandmother', 'uncle', 'aunt', 'cousin', 'nephew', 'niece',
        'husband', 'wife', 'spouse',
        'мать', 'отец', 'родитель', 'сын', 'дочь', 'ребёнок', 'брат', 'сестра',
        'дед', 'бабушка', 'дядя', 'тётя', 'двоюродный', 'племянник', 'муж', 'жена',
    ],
    'food': [
        'bread', 'cheese', 'butter', 'milk', 'meat', 'fish', 'egg', 'flour', 'salt',
        'sugar', 'oil', 'soup', 'porridge', 'cake', 'honey', 'food', 'meal', 'dish',
        'хлеб', 'сыр', 'масло', 'молоко', 'мясо', 'яйцо', 'мука', 'соль', 'сахар',
        'суп', 'каша', 'торт', 'мёд', 'еда', 'пища', 'блюдо',
    ],
    'tool': [
        'knife', 'axe', 'hammer', 'saw', 'shovel', 'hoe', 'rake', 'sickle', 'scythe',
        'needle', 'scissors', 'spoon', 'fork', 'plate', 'pot', 'pan', 'bucket',
        'rope', 'chain', 'hook', 'nail', 'key', 'lock', 'tool', 'instrument',
        'нож', 'топор', 'молоток', 'пила', 'лопата', 'мотыга', 'грабли', 'серп',
        'коса', 'игла', 'ножницы', 'ложка', 'вилка', 'тарелка', 'кастрюля',
        'ведро', 'верёвка', 'цепь', 'крюк', 'гвоздь', 'ключ', 'замок',
    ],
    'clothing': [
        'shirt', 'dress', 'coat', 'jacket', 'pants', 'skirt', 'shoe', 'boot', 'hat',
        'cap', 'scarf', 'glove', 'sock', 'belt', 'button', 'clothes', 'garment',
        'рубашка', 'платье', 'пальто', 'куртка', 'штаны', 'юбка', 'обувь', 'ботинок',
        'шапка', 'шарф', 'перчатка', 'носок', 'ремень', 'пуговица', 'одежда',
    ],
    'house': [
        'house', 'home', 'room', 'door', 'window', 'wall', 'roof', 'floor', 'ceiling',
        'stairs', 'fireplace', 'chimney', 'fence', 'gate', 'yard',
        'дом', 'комната', 'дверь', 'окно', 'стена', 'крыша', 'пол', 'потолок',
        'лестница', 'камин', 'труба', 'забор', 'ворота', 'двор',
    ],
    'settlement': [
        'village', 'town', 'city', 'settlement', 'hamlet',
        'село', 'деревня', 'город', 'посёлок', 'поселение',
    ],
    'time': [
        'morning', 'evening', 'night', 'day', 'noon', 'midnight', 'dawn', 'dusk',
        'today', 'yesterday', 'tomorrow', 'week', 'month', 'year', 'season',
        'spring', 'summer', 'autumn', 'winter', 'time', 'hour', 'minute',
        'утро', 'вечер', 'ночь', 'день', 'полдень', 'полночь', 'рассвет', 'закат',
        'сегодня', 'вчера', 'завтра', 'неделя', 'месяц', 'год', 'время', 'час',
    ],
    'color': [
        'white', 'black', 'red', 'blue', 'green', 'yellow', 'brown', 'gray', 'color',
        'белый', 'чёрный', 'красный', 'синий', 'зелёный', 'жёлтый', 'коричневый',
        'серый', 'цвет',
    ],
    'emotion': [
        'happy', 'sad', 'angry', 'afraid', 'love', 'hate', 'joy', 'sorrow', 'fear',
        'hope', 'shame', 'pride', 'envy', 'pity',
        'счастливый', 'грустный', 'злой', 'любовь', 'ненависть', 'радость',
        'горе', 'страх', 'надежда', 'стыд', 'гордость', 'зависть', 'жалость',
    ],
    'occupation': [
        'smith', 'carpenter', 'shoemaker', 'tailor', 'weaver', 'potter', 'baker',
        'butcher', 'shepherd', 'farmer', 'hunter', 'fisherman', 'teacher', 'doctor',
        'worker', 'craftsman',
        'кузнец', 'плотник', 'сапожник', 'портной', 'ткач', 'гончар', 'пекарь',
        'мясник', 'пастух', 'фермер', 'охотник', 'рыбак', 'учитель', 'врач',
    ],
    'agriculture': [
        'plow', 'sow', 'harvest', 'field', 'farm', 'grain', 'wheat', 'barley', 'corn',
        'seed', 'crop',
        'плуг', 'сеять', 'жатва', 'поле', 'ферма', 'зерно', 'пшеница', 'ячмень',
        'кукуруза', 'семя', 'урожай',
    ],
    'warfare': [
        'sword', 'knife', 'spear', 'arrow', 'bow', 'shield', 'armor', 'weapon', 'war',
        'battle', 'fight', 'soldier', 'warrior',
        'меч', 'копьё', 'стрела', 'лук', 'щит', 'доспехи', 'оружие', 'война',
        'битва', 'боец', 'воин', 'солдат',
    ],
    'religion': [
        'god', 'prayer', 'mosque', 'church', 'holy', 'sacred', 'priest', 'imam',
        'heaven', 'hell', 'sin', 'soul', 'spirit', 'angel', 'demon', 'devil',
        'бог', 'молитва', 'мечеть', 'церковь', 'святой', 'священный', 'священник',
        'имам', 'рай', 'ад', 'грех', 'душа', 'дух', 'ангел', 'демон', 'дьявол',
        'dragon', 'дракон',
    ],
    'measure': [
        'meter', 'kilogram', 'liter', 'measure', 'weight', 'length', 'size', 'quantity',
        'метр', 'килограмм', 'литр', 'мера', 'вес', 'длина', 'размер', 'количество',
    ],
}


def suggest_tags(translation_en, translation_ru):
    """Suggest semantic tags based on translation text."""
    suggestions = set()

    # Combine English and Russian translations
    text = f"{translation_en or ''} {translation_ru or ''}".lower()

    # Check each tag pattern
    for tag, keywords in TAG_PATTERNS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                suggestions.add(tag)
                break  # One match per tag is enough

    return sorted(suggestions)


def analyze_file(yaml_file):
    """Analyze a file and return missing tag suggestions."""
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data or 'definitions' not in data:
            return []

        suggestions = []

        for i, defn in enumerate(data['definitions']):
            if not isinstance(defn, dict):
                continue

            # Check if definition already has semantic tags
            existing_tags = defn.get('tags', [])
            has_semantic = any(tag in TAG_PATTERNS for tag in existing_tags)

            if has_semantic:
                continue  # Already has semantic tags

            # Get translations
            translation = defn.get('translation', {})
            en = translation.get('en', '')
            ru = translation.get('ru', '')

            # Suggest tags
            suggested = suggest_tags(en, ru)

            if suggested:
                suggestions.append({
                    'file': yaml_file,
                    'headword': data.get('headword', '?'),
                    'definition_index': i,
                    'translation_en': en,
                    'translation_ru': ru,
                    'existing_tags': existing_tags,
                    'suggested_tags': suggested,
                })

        return suggestions

    except Exception as e:
        return []


def main():
    lexicon_dir = Path('lexicon')

    print("Semantic Tag Suggestion Report")
    print("=" * 80)
    print("Analyzing definitions without semantic tags...\n")

    all_suggestions = []

    for yaml_file in lexicon_dir.rglob('*.yaml'):
        suggestions = analyze_file(yaml_file)
        all_suggestions.extend(suggestions)

    # Group by suggested tag
    by_tag = defaultdict(list)
    for sugg in all_suggestions:
        for tag in sugg['suggested_tags']:
            by_tag[tag].append(sugg)

    # Print summary
    print(f"Found {len(all_suggestions)} definitions without semantic tags")
    print(f"Suggestions for {len(by_tag)} different tags\n")
    print("=" * 80)

    # Print detailed suggestions
    for tag in sorted(by_tag.keys()):
        items = by_tag[tag]
        print(f"\n### {tag.upper()} ({len(items)} suggestions)")
        print("-" * 80)

        for item in items[:20]:  # Show first 20 per tag
            print(f"  {item['headword']:20} {item['translation_en']:30} | {item['translation_ru']}")
            print(f"    File: {item['file'].relative_to(lexicon_dir)}")
            if item['existing_tags']:
                print(f"    Existing tags: {', '.join(item['existing_tags'])}")
            print(f"    → Suggest: {', '.join(item['suggested_tags'])}")
            print()

        if len(items) > 20:
            print(f"  ... and {len(items) - 20} more\n")

    print("\n" + "=" * 80)
    print(f"\nTotal: {len(all_suggestions)} definitions need semantic tags")
    print("\nNext steps:")
    print("  1. Review suggestions above")
    print("  2. Manually add appropriate tags to lexicon files")
    print("  3. Re-run this script to check progress")


if __name__ == '__main__':
    main()
