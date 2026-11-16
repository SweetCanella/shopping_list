-- Получение списка всех товаров
SELECT
    id,
    name,
    quantity
FROM products
ORDER BY name;

-- Поиск товаров по количеству
SELECT
    id,
    name,
    quantity
FROM products
WHERE quantity >= 2
ORDER BY quantity;

-- Активные позиции списка
SELECT
    id,
    product_id,
    user_id,
    purchase_date
FROM purchases
WHERE is_cancelled = 0
ORDER BY purchase_date;

-- Полная информация о позиции списка
SELECT
    purchases.id,
    purchases.purchase_date,
    products.name AS product_name,
    products.quantity,
    users.name AS user_name,
    users.email
FROM purchases
JOIN products
    ON purchases.product_id = products.id
JOIN users
    ON purchases.user_id = users.id
WHERE purchases.is_cancelled = 0
ORDER BY purchases.purchase_date;

-- Свободные товары на выбранную дату
SELECT
    products.id,
    products.name,
    products.quantity
FROM products
WHERE products.id NOT IN (
    SELECT purchases.product_id
    FROM purchases
    WHERE purchases.purchase_date = '2026-09-20'
        AND purchases.is_cancelled = 0
)
ORDER BY products.name;

-- Количество активных позиций
SELECT
    COUNT(*) AS purchases_count
FROM purchases
WHERE is_cancelled = 0;

-- Количество позиций по товарам
SELECT
    products.name AS product_name,
    COUNT(purchases.id) AS purchases_count
FROM products
LEFT JOIN purchases
    ON products.id = purchases.product_id
    AND purchases.is_cancelled = 0
GROUP BY products.id, products.name
ORDER BY purchases_count DESC;

-- Список пользователей
SELECT
    id,
    name,
    email
FROM users
ORDER BY name;

-- Позиции выбранного пользователя
SELECT
    purchases.id,
    purchases.purchase_date,
    products.name AS product_name,
    users.name AS user_name
FROM purchases
JOIN products
    ON purchases.product_id = products.id
JOIN users
    ON purchases.user_id = users.id
WHERE purchases.user_id = 1
    AND purchases.is_cancelled = 0
ORDER BY purchases.purchase_date;

-- Товары с количеством позиций больше заданного
SELECT
    products.name AS product_name,
    COUNT(purchases.id) AS purchases_count
FROM products
JOIN purchases
    ON products.id = purchases.product_id
WHERE purchases.is_cancelled = 0
GROUP BY products.id, products.name
HAVING COUNT(purchases.id) > 1
ORDER BY purchases_count DESC;
