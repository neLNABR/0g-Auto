document.addEventListener('DOMContentLoaded', function() {
    // Загружаем конфигурацию при загрузке страницы
    fetchConfig();
    
    // Обработчик для кнопки сохранения
    document.getElementById('saveButton').addEventListener('click', saveConfig);
    
    // Обработчики для пунктов меню
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.addEventListener('click', function() {
            // Убираем активный класс у всех пунктов
            document.querySelectorAll('.sidebar-item').forEach(i => i.classList.remove('active'));
            // Добавляем активный класс текущему пункту
            this.classList.add('active');
            
            // Показываем соответствующую секцию
            const section = this.dataset.section;
            document.querySelectorAll('.config-section').forEach(s => s.classList.remove('active'));
            document.getElementById(`${section}-section`).classList.add('active');
        });
    });
});

// Функция для форматирования названий полей
function formatFieldName(name) {
    // Заменяем подчеркивания на пробелы
    let formatted = name.replace(/_/g, ' ');
    
    // Делаем первую букву заглавной, остальные строчными
    return formatted.charAt(0).toUpperCase() + formatted.slice(1).toLowerCase();
}

// Функция для загрузки конфигурации с сервера
async function fetchConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();
        renderConfig(config);
    } catch (error) {
        showNotification('Failed to load configuration: ' + error.message, 'error');
    }
}

// Функция для сохранения конфигурации
async function saveConfig() {
    try {
        const config = collectFormData();
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showNotification('Configuration saved successfully!', 'success');
        } else {
            showNotification('Error: ' + result.message, 'error');
        }
    } catch (error) {
        showNotification('Failed to save configuration: ' + error.message, 'error');
    }
}

// Функция для сбора данных формы
function collectFormData() {
    config = {}
    
    // Собираем данные из всех полей ввода
    document.querySelectorAll('[data-config-path]').forEach(element => {
        const path = element.dataset.configPath.split('.');
        let current = config;
        
        // Создаем вложенные объекты по пути
        for (let i = 0; i < path.length - 1; i++) {
            if (!current[path[i]]) {
                current[path[i]] = {};
            }
            current = current[path[i]];
        }
        
        const lastKey = path[path.length - 1];
        
        if (element.type === 'checkbox') {
            current[lastKey] = element.checked;
        } else if (element.classList.contains('network-checkbox-container')) {
            const selectedNetworks = Array.from(element.querySelectorAll('input[type="checkbox"]:checked'))
                .map(checkbox => checkbox.value);
            current[lastKey] = selectedNetworks;
        } else if (element.classList.contains('tags-input')) {
            // Обработка полей с тегами (например, для RPCS, NETWORKS_TO_REFUEL_FROM, EXCHANGES.withdrawals.networks)
            const tags = Array.from(element.querySelectorAll('.tag-text'))
                .map(tag => tag.textContent.trim());
            current[lastKey] = tags;
        } else if (element.classList.contains('range-min')) {
            const rangeKey = lastKey.replace('_MIN', '');
            if (!current[rangeKey]) {
                current[rangeKey] = [0, 0];
            }
            // Parse as float or int based on data-type attribute
            const parseFunc = element.dataset.type === 'float' ? parseFloat : parseInt;
            current[rangeKey][0] = parseFunc(element.value);
        } else if (element.classList.contains('range-max')) {
            const rangeKey = lastKey.replace('_MAX', '');
            if (!current[rangeKey]) {
                current[rangeKey] = [0, 0];
            }
            // Parse as float or int based on data-type attribute
            const parseFunc = element.dataset.type === 'float' ? parseFloat : parseInt;
            current[rangeKey][1] = parseFunc(element.value);
        } else if (element.classList.contains('list-input')) {
            // Для списков (разделенных запятыми)
            current[lastKey] = element.value.split(',')
                .map(item => item.trim())
                .filter(item => item !== '');
                
            // Преобразуем в числа, если это числовой список
            if (element.dataset.type === 'number-list') {
                current[lastKey] = current[lastKey].map(item => parseInt(item));
            }
        } else {
            // Для обычных полей
            if (element.dataset.type === 'number') {
                current[lastKey] = parseInt(element.value);
            } else if (element.dataset.type === 'float') {
                current[lastKey] = parseFloat(element.value);
            } else {
                current[lastKey] = element.value;
            }
        }
    });
    
    return config;
}

// Функция для отображения конфигурации
function renderConfig(config) {
    const container = document.getElementById('configContainer');
    container.innerHTML = ''; // Очищаем контейнер
    
    // Создаем секции для каждой категории
    const sections = {
        'settings': { key: 'SETTINGS', title: 'Settings', icon: 'cog' },
        'flow': { key: 'FLOW', title: 'Flow', icon: 'exchange-alt' },
        'swaps': { key: 'ZERO_EXCHANGE_SWAPS', title: 'Zero Exchange Swaps', icon: 'sync' },
        'captcha': { key: 'CAPTCHA', title: 'Captcha', icon: 'robot' },
        'rpcs': { key: 'RPCS', title: 'RPCs', icon: 'network-wired' },
        'puzzlemania': { key: 'PUZZLEMANIA', title: 'Puzzlemania', icon: 'puzzle-piece' },
        'crustyswap': { key: 'CRUSTY_SWAP', title: 'Crusty Swap', icon: 'gas-pump' },
        'exchanges': { key: 'EXCHANGES', title: 'Exchanges', icon: 'university' },
        'others': { key: 'OTHERS', title: 'Others', icon: 'ellipsis-h' }
    };
    
    // Создаем все секции
    Object.entries(sections).forEach(([sectionId, { key, title, icon }], index) => {
        const section = document.createElement('div');
        section.id = `${sectionId}-section`;
        section.className = `config-section ${index === 0 ? 'active' : ''}`;
        
        const sectionTitle = document.createElement('h2');
        sectionTitle.className = 'section-title';
        sectionTitle.innerHTML = `<i class="fas fa-${icon}"></i> ${title}`;
        section.appendChild(sectionTitle);
        
        const cardsContainer = document.createElement('div');
        cardsContainer.className = 'config-cards';
        section.appendChild(cardsContainer);
        
        // Заполняем секцию данными
        if (config[key]) {
            if (key === 'SETTINGS') {
                // Карточка для основных настроек
                createCard(cardsContainer, 'Basic Settings', 'sliders-h', [
                    { key: 'THREADS', value: config[key]['THREADS'] },
                    { key: 'ATTEMPTS', value: config[key]['ATTEMPTS'] },
                    { key: 'SHUFFLE_WALLETS', value: config[key]['SHUFFLE_WALLETS'] },
                    { key: 'WAIT_FOR_TRANSACTION_CONFIRMATION_IN_SECONDS', value: config[key]['WAIT_FOR_TRANSACTION_CONFIRMATION_IN_SECONDS'] }
                ], key);
                
                // Карточка для диапазонов аккаунтов
                createCard(cardsContainer, 'Account Settings', 'users', [
                    { key: 'ACCOUNTS_RANGE', value: config[key]['ACCOUNTS_RANGE'] },
                    { key: 'EXACT_ACCOUNTS_TO_USE', value: config[key]['EXACT_ACCOUNTS_TO_USE'], isSpaceList: true }
                ], key);
                
                // Карточка для пауз
                createCard(cardsContainer, 'Timing Settings', 'clock', [
                    { key: 'PAUSE_BETWEEN_ATTEMPTS', value: config[key]['PAUSE_BETWEEN_ATTEMPTS'] },
                    { key: 'PAUSE_BETWEEN_SWAPS', value: config[key]['PAUSE_BETWEEN_SWAPS'] },
                    { key: 'RANDOM_PAUSE_BETWEEN_ACCOUNTS', value: config[key]['RANDOM_PAUSE_BETWEEN_ACCOUNTS'] },
                    { key: 'RANDOM_PAUSE_BETWEEN_ACTIONS', value: config[key]['RANDOM_PAUSE_BETWEEN_ACTIONS'] },
                    { key: 'RANDOM_INITIALIZATION_PAUSE', value: config[key]['RANDOM_INITIALIZATION_PAUSE'] }
                ], key);
                
                // Карточка для Telegram
                createCard(cardsContainer, 'Telegram Settings', 'paper-plane', [
                    { key: 'SEND_TELEGRAM_LOGS', value: config[key]['SEND_TELEGRAM_LOGS'] },
                    { key: 'TELEGRAM_BOT_TOKEN', value: config[key]['TELEGRAM_BOT_TOKEN'] },
                    { key: 'TELEGRAM_USERS_IDS', value: config[key]['TELEGRAM_USERS_IDS'], isSpaceList: true }
                ], key);
            } else if (key === 'CAPTCHA') {
                // Специальная обработка для Captcha
                createCard(cardsContainer, 'Captcha Settings', 'robot', [
                    { key: 'SOLVIUM_API_KEY', value: config[key]['SOLVIUM_API_KEY'] },
                    { key: 'NOCAPTCHA_API_KEY', value: config[key]['NOCAPTCHA_API_KEY'] },
                    { key: 'USE_NOCAPTCHA', value: config[key]['USE_NOCAPTCHA'], isCheckbox: true }
                ], key);
            } else if (key === 'PUZZLEMANIA') {
                // Специальная обработка для Puzzlemania
                createCard(cardsContainer, 'Puzzlemania Settings', 'puzzle-piece', [
                    { key: 'USE_REFERRAL_CODE', value: config[key]['USE_REFERRAL_CODE'], isCheckbox: true },
                    { key: 'INVITES_PER_REFERRAL_CODE', value: config[key]['INVITES_PER_REFERRAL_CODE'] },
                    { key: 'COLLECT_REFERRAL_CODE', value: config[key]['COLLECT_REFERRAL_CODE'], isCheckbox: true }
                ], key);
            } else if (key === 'ZERO_EXCHANGE_SWAPS') {
                // Специальная обработка для Zero Exchange Swaps
                createCard(cardsContainer, 'Zero Exchange Swaps Settings', 'sync', [
                    { key: 'BALANCE_PERCENT_TO_SWAP', value: config[key]['BALANCE_PERCENT_TO_SWAP'] },
                    { key: 'NUMBER_OF_SWAPS', value: config[key]['NUMBER_OF_SWAPS'] }
                ], key);
            } else if (key === 'FLOW') {
                // Специальная обработка для Flow
                createCard(cardsContainer, 'Flow Settings', 'exchange-alt', [
                    { key: 'SKIP_FAILED_TASKS', value: config[key]['SKIP_FAILED_TASKS'], isCheckbox: true }
                ], key);
            } else if (key === 'RPCS') {
                // Специальная обработка для RPCs
                createCard(cardsContainer, 'RPC Settings', 'network-wired', 
                    Object.entries(config[key]).map(([k, v]) => ({ 
                        key: k, 
                        value: v, 
                        isList: true,
                        isArray: true
                    })), 
                    key
                );
            } else if (key === 'OTHERS') {
                // Специальная обработка для Other Settings
                createCard(cardsContainer, 'Other Settings', 'ellipsis-h', [
                    { key: 'SKIP_SSL_VERIFICATION', value: config[key]['SKIP_SSL_VERIFICATION'], isCheckbox: true },
                    { key: 'USE_PROXY_FOR_RPC', value: config[key]['USE_PROXY_FOR_RPC'], isCheckbox: true }
                ], key);
            } else if (key === 'CRUSTY_SWAP') {
                createCard(cardsContainer, 'Crusty Swap Settings', 'gas-pump', [
                    { key: 'NETWORKS_TO_REFUEL_FROM', value: config[key]['NETWORKS_TO_REFUEL_FROM'], isNetworkSelection: true },
                    { key: 'AMOUNT_TO_REFUEL', value: config[key]['AMOUNT_TO_REFUEL'], isFloat: true },
                    { key: 'MINIMUM_BALANCE_TO_REFUEL', value: config[key]['MINIMUM_BALANCE_TO_REFUEL'], isFloat: true },
                    { key: 'WAIT_FOR_FUNDS_TO_ARRIVE', value: config[key]['WAIT_FOR_FUNDS_TO_ARRIVE'], isCheckbox: true },
                    { key: 'MAX_WAIT_TIME', value: config[key]['MAX_WAIT_TIME'] },
                    { key: 'BRIDGE_ALL', value: config[key]['BRIDGE_ALL'], isCheckbox: true },
                    { key: 'BRIDGE_ALL_MAX_AMOUNT', value: config[key]['BRIDGE_ALL_MAX_AMOUNT'], isFloat: true }
                ], key);
            } else if (key === 'EXCHANGES') {
                // General Exchange Settings
                createCard(cardsContainer, 'Exchange Details', 'info-circle', [
                    { key: 'name', value: config[key]['name'], isSelect: true, options: ['OKX', 'BITGET'] },
                    { key: 'apiKey', value: config[key]['apiKey'] },
                    { key: 'secretKey', value: config[key]['secretKey'] },
                    { key: 'passphrase', value: config[key]['passphrase'] }
                ], key);

                // Withdrawals - Create a card for each withdrawal config
                if (config[key]['withdrawals'] && Array.isArray(config[key]['withdrawals'])) {
                     const withdrawalsCard = document.createElement('div');
                     withdrawalsCard.className = 'config-card';
                     const withdrawalsTitle = document.createElement('div');
                     withdrawalsTitle.className = 'card-title';
                     withdrawalsTitle.innerHTML = '<i class="fas fa-money-bill-wave"></i> Withdrawals';
                     withdrawalsCard.appendChild(withdrawalsTitle);

                     config[key]['withdrawals'].forEach((withdrawal, index) => {
                        const withdrawalGroup = document.createElement('div');
                        withdrawalGroup.style.border = '1px solid rgba(255, 255, 255, 0.1)';
                        withdrawalGroup.style.borderRadius = '8px';
                        withdrawalGroup.style.padding = '15px';
                        withdrawalGroup.style.marginBottom = '15px';

                        const groupTitle = document.createElement('h4');
                        groupTitle.textContent = `Withdrawal ${index + 1} (${withdrawal.currency || 'N/A'})`;
                        groupTitle.style.marginBottom = '10px';
                        groupTitle.style.color = 'var(--neon-cyan)';
                        withdrawalGroup.appendChild(groupTitle);

                        // Create fields for each withdrawal property
                        createTextField(withdrawalGroup, 'currency', withdrawal.currency, `${key}.withdrawals[${index}].currency`);
                        createNetworkSelectionField(withdrawalGroup, 'networks', withdrawal.networks, `${key}.withdrawals[${index}].networks`);
                        createTextField(withdrawalGroup, 'min_amount', withdrawal.min_amount, `${key}.withdrawals[${index}].min_amount`, true);
                        createTextField(withdrawalGroup, 'max_amount', withdrawal.max_amount, `${key}.withdrawals[${index}].max_amount`, true);
                        createTextField(withdrawalGroup, 'max_balance', withdrawal.max_balance, `${key}.withdrawals[${index}].max_balance`, true);
                        createCheckboxField(withdrawalGroup, 'wait_for_funds', withdrawal.wait_for_funds, `${key}.withdrawals[${index}].wait_for_funds`);
                        createTextField(withdrawalGroup, 'max_wait_time', withdrawal.max_wait_time, `${key}.withdrawals[${index}].max_wait_time`);
                        createTextField(withdrawalGroup, 'retries', withdrawal.retries, `${key}.withdrawals[${index}].retries`);

                        withdrawalsCard.appendChild(withdrawalGroup);
                     });
                     cardsContainer.appendChild(withdrawalsCard);
                }
            } else {
                // Остальные категории
                createCard(cardsContainer, `${title} Settings`, icon, 
                    Object.entries(config[key]).map(([k, v]) => ({ key: k, value: v })), 
                    key
                );
            }
        }
        
        container.appendChild(section);
    });
}

// Функция для создания карточки
function createCard(container, title, iconClass, fields, category) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'config-card';
    
    const titleDiv = document.createElement('div');
    titleDiv.className = 'card-title';
    
    const icon = document.createElement('i');
    icon.className = `fas fa-${iconClass}`;
    titleDiv.appendChild(icon);
    
    const titleText = document.createElement('span');
    titleText.textContent = title;
    titleDiv.appendChild(titleText);
    
    cardDiv.appendChild(titleDiv);
    
    fields.forEach(({ key, value, isList, isSpaceList, isFloat, isCheckbox, isNetworkSelection, isSelect, options }) => {
        if (isCheckbox || (typeof value === 'boolean' && isCheckbox === undefined)) {
            createCheckboxField(cardDiv, key, value, `${category}.${key}`);
        } else if (Array.isArray(value) && value.length === 2 && (typeof value[0] === 'number' || typeof value[0] === 'string') && (typeof value[1] === 'number' || typeof value[1] === 'string') && !isList && !isSpaceList && !isNetworkSelection) {
            createRangeField(cardDiv, key, value, `${category}.${key}`, isFloat);
        } else if (isNetworkSelection) {
            createNetworkSelectionField(cardDiv, key, value, `${category}.${key}`);
        } else if (isList) {
            createTagsField(cardDiv, key, value, `${category}.${key}`, false);
        } else if (isSpaceList) {
            createTagsField(cardDiv, key, value, `${category}.${key}`, true);
        } else if (isSelect) {
            createSelectField(cardDiv, key, value, options, `${category}.${key}`);
        } else if (Array.isArray(value)) {
            createListField(cardDiv, key, value, `${category}.${key}`);
        } else {
            createTextField(cardDiv, key, value, `${category}.${key}`);
        }
    });
    
    container.appendChild(cardDiv);
}

// Создание текстового поля
function createTextField(container, key, value, path, isFloat = false) {
    const fieldDiv = document.createElement('div');
    fieldDiv.className = 'config-field';
    
    const label = document.createElement('label');
    label.className = 'field-label';
    label.textContent = formatFieldName(key);
    fieldDiv.appendChild(label);
    
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'field-input';
    input.value = value;
    input.dataset.configPath = path;
    
    // Добавляем подсказку для API ключей
    if (key.toLowerCase().includes('key')) {
        const tooltip = document.createElement('span');
        tooltip.className = 'tooltip';
        tooltip.innerHTML = '?<span class="tooltip-text">Enter your API key here</span>';
        label.appendChild(tooltip);
    }
    
    if (typeof value === 'number' && !isFloat) {
        input.dataset.type = 'number';
        input.type = 'number';
        input.className += ' small-input';
    } else if (typeof value === 'number' && isFloat) {
        input.dataset.type = 'float';
        input.type = 'number';
        input.step = 'any';
        input.className += ' small-input';
    } else if (key.toLowerCase().includes('key') || key.toLowerCase().includes('token') || key.toLowerCase().includes('passphrase')) {
        input.type = 'password';
    }
    
    fieldDiv.appendChild(input);
    container.appendChild(fieldDiv);
}

// Создание поля диапазона
function createRangeField(container, key, value, path, isFloat = false) {
    const fieldDiv = document.createElement('div');
    fieldDiv.className = 'config-field';
    
    const label = document.createElement('label');
    label.className = 'field-label';
    label.textContent = formatFieldName(key);
    fieldDiv.appendChild(label);
    
    const rangeDiv = document.createElement('div');
    rangeDiv.className = 'range-input';
    
    const minInput = document.createElement('input');
    minInput.type = 'number';
    minInput.className = 'field-input range-min small-input';
    minInput.value = value[0];
    minInput.dataset.configPath = `${path}_MIN`;
    minInput.dataset.type = isFloat ? 'float' : 'number';
    if (isFloat) minInput.step = 'any';
    
    const separator = document.createElement('span');
    separator.className = 'range-separator';
    separator.textContent = '-';
    
    const maxInput = document.createElement('input');
    maxInput.type = 'number';
    maxInput.className = 'field-input range-max small-input';
    maxInput.value = value[1];
    maxInput.dataset.configPath = `${path}_MAX`;
    maxInput.dataset.type = isFloat ? 'float' : 'number';
    if (isFloat) maxInput.step = 'any';
    
    rangeDiv.appendChild(minInput);
    rangeDiv.appendChild(separator);
    rangeDiv.appendChild(maxInput);
    
    fieldDiv.appendChild(rangeDiv);
    container.appendChild(fieldDiv);
}

// Создание чекбокса
function createCheckboxField(container, key, value, path) {
    const fieldDiv = document.createElement('div');
    fieldDiv.className = 'checkbox-field';
    
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.className = 'checkbox-input';
    input.checked = value;
    input.dataset.configPath = path;
    input.id = `checkbox-${path.replace(/\./g, '-')}`;
    
    const label = document.createElement('label');
    label.className = 'checkbox-label';
    label.textContent = formatFieldName(key);
    label.htmlFor = input.id;
    
    fieldDiv.appendChild(input);
    fieldDiv.appendChild(label);
    container.appendChild(fieldDiv);
}

// Создание списка
function createListField(container, key, value, path) {
    const fieldDiv = document.createElement('div');
    fieldDiv.className = 'config-field';
    
    const label = document.createElement('label');
    label.className = 'field-label';
    label.textContent = formatFieldName(key);
    fieldDiv.appendChild(label);
    
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'field-input list-input';
    input.value = value.join(', ');
    input.dataset.configPath = path;
    
    // Определяем, является ли это списком чисел
    if (value.length > 0 && typeof value[0] === 'number') {
        input.dataset.type = 'number-list';
    }
    
    fieldDiv.appendChild(input);
    container.appendChild(fieldDiv);
}

// Создание поля с тегами (для списков)
function createTagsField(container, key, value, path, useSpaces) {
    const fieldDiv = document.createElement('div');
    fieldDiv.className = 'config-field';
    
    const label = document.createElement('label');
    label.className = 'field-label';
    label.textContent = formatFieldName(key);
    fieldDiv.appendChild(label);
    
    const tagsContainer = document.createElement('div');
    tagsContainer.className = 'tags-input';
    tagsContainer.dataset.configPath = path;
    tagsContainer.dataset.useSpaces = useSpaces ? 'true' : 'false';
    
    // Убедимся, что value является массивом
    const values = Array.isArray(value) ? value : [value];
    
    // Добавляем существующие теги
    values.forEach(item => {
        const tag = createTag(item.toString());
        tagsContainer.appendChild(tag);
    });
    
    // Добавляем поле ввода для новых тегов
    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Add item...';
    
    // Обработчик для добавления нового тега
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ' && useSpaces) {
            e.preventDefault();
            const value = this.value.trim();
            if (value) {
                const tag = createTag(value);
                tagsContainer.insertBefore(tag, this);
                this.value = '';
            }
        }
    });
    
    tagsContainer.appendChild(input);
    
    // Функция для создания тега
    function createTag(text) {
        const tag = document.createElement('div');
        tag.className = 'tag';
        
        const tagText = document.createElement('span');
        tagText.className = 'tag-text';
        tagText.textContent = text;
        
        const removeBtn = document.createElement('button');
        removeBtn.className = 'tag-remove';
        removeBtn.innerHTML = '&times;';
        removeBtn.addEventListener('click', function() {
            tag.remove();
        });
        
        tag.appendChild(tagText);
        tag.appendChild(removeBtn);
        
        return tag;
    }
    
    fieldDiv.appendChild(tagsContainer);
    container.appendChild(fieldDiv);
}

// Функция для отображения уведомления
function showNotification(message, type) {
    const notification = document.getElementById('notification');
    notification.className = `notification ${type} show`;
    
    document.getElementById('notification-message').textContent = message;
    
    setTimeout(() => {
        notification.className = 'notification';
    }, 3000);
}

// --- New Helper Function for Network Selection ---
function createNetworkSelectionField(container, key, currentValues, path) {
    const fieldDiv = document.createElement('div');
    fieldDiv.className = 'config-field';

    const label = document.createElement('label');
    label.className = 'field-label';
    label.textContent = formatFieldName(key);
    fieldDiv.appendChild(label);

    const checkboxContainer = document.createElement('div');
    checkboxContainer.dataset.configPath = path;
    checkboxContainer.className = 'network-checkbox-container';
    checkboxContainer.style.display = 'flex';
    checkboxContainer.style.gap = '15px';
    checkboxContainer.style.marginTop = '10px';

    const allowedNetworks = ["Arbitrum", "Optimism", "Base"];

    // Ensure currentValues is an array
    const selectedValues = Array.isArray(currentValues) ? currentValues : [];

    allowedNetworks.forEach(network => {
        const wrapper = document.createElement('div');
        wrapper.style.display = 'flex';
        wrapper.style.alignItems = 'center';
        wrapper.style.gap = '5px';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = network;
        checkbox.id = `${path}-${network}`.replace(/\.|\\[|\\]/g, '-');
        checkbox.checked = selectedValues.includes(network);
        checkbox.className = 'checkbox-input';
        checkbox.style.width = '20px';
        checkbox.style.height = '20px';

        const checkboxLabel = document.createElement('label');
        checkboxLabel.textContent = network;
        checkboxLabel.htmlFor = checkbox.id;
        checkboxLabel.className = 'checkbox-label';

        wrapper.appendChild(checkbox);
        wrapper.appendChild(checkboxLabel);
        checkboxContainer.appendChild(wrapper);
    });

    fieldDiv.appendChild(checkboxContainer);
    container.appendChild(fieldDiv);
}

// --- New Helper Function for Select Field ---
function createSelectField(container, key, currentValue, options, path) {
    const fieldDiv = document.createElement('div');
    fieldDiv.className = 'config-field';

    const label = document.createElement('label');
    label.className = 'field-label';
    label.textContent = formatFieldName(key);
    fieldDiv.appendChild(label);

    const select = document.createElement('select');
    select.className = 'field-input'; // Use existing styling
    select.dataset.configPath = path;

    options.forEach(optionValue => {
        const option = document.createElement('option');
        option.value = optionValue;
        option.textContent = optionValue;
        if (optionValue === currentValue) {
            option.selected = true;
        }
        select.appendChild(option);
    });

    fieldDiv.appendChild(select);
    container.appendChild(fieldDiv);
}
