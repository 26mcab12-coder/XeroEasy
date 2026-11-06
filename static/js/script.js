/**
 * XeroEasy - Smart Campus Reprographics Client Engine
 * Role-Adapted Architecture:
 * - Admin Dashboard: ONLY Order Details and Activity Trends!
 * - Student Dashboard: Print Desk, My Orders, Services, Pickup Hubs, Help.
 */

// DOM Elements: Authentication
const authView = document.getElementById('auth-view');
const dashboardView = document.getElementById('dashboard-view');
const authForm = document.getElementById('auth-form');
const switchMode = document.getElementById('switch-mode');
const authTitle = document.getElementById('auth-title');
const authSubtitle = document.getElementById('auth-subtitle');
const authEyebrow = document.getElementById('auth-eyebrow');
const authSubmit = document.getElementById('auth-submit');
const nameField = document.getElementById('name-field');
const phoneField = document.getElementById('phone-field');
const formMessage = document.getElementById('form-message');
const roleInput = document.getElementById('role');
const forgotLink = document.getElementById('forgot-link');
const forgotModal = document.getElementById('forgot-modal');
const closeForgot = document.getElementById('close-forgot');
const dismissForgot = document.getElementById('dismiss-forgot');

// DOM Elements: Header & Navigation
const signOut = document.getElementById('sign-out');
const addExpense = document.getElementById('add-expense');
const btnNotifications = document.getElementById('btn-notifications');
const notificationsModal = document.getElementById('notifications-modal');
const closeNotifications = document.getElementById('close-notifications');
const notificationsList = document.getElementById('notifications-list');
const navOrderCount = document.getElementById('nav-order-count');
const appDeskTag = document.getElementById('app-desk-tag');
const navOrdersLabel = document.getElementById('nav-orders-label');

// DOM Elements: Print Studio & Quick Order
const orderModal = document.getElementById('order-modal');
const closeOrder = document.getElementById('close-order');
const modalGoToDesk = document.getElementById('modal-go-to-desk');
const orderForm = document.getElementById('order-form');
const serviceSelect = document.getElementById('service');
const copiesInput = document.getElementById('copies');
const copiesMinus = document.getElementById('copies-minus');
const copiesPlus = document.getElementById('copies-plus');
const collectionSelect = document.getElementById('collection');
const calcRate = document.getElementById('calc-rate');
const calcCopies = document.getElementById('calc-copies');
const calcTotal = document.getElementById('calc-total');
const fileDropzone = document.getElementById('file-dropzone');
const orderFileInput = document.getElementById('order-file');
const dropzonePrompt = document.getElementById('dropzone-prompt');
const filePreview = document.getElementById('file-preview');
const previewFilename = document.getElementById('preview-filename');
const previewFilesize = document.getElementById('preview-filesize');
const removeFileBtn = document.getElementById('remove-file');
const activeJobBanner = document.getElementById('active-job-banner');
const activeJobTitle = document.getElementById('active-job-title');
const activeJobDesc = document.getElementById('active-job-desc');
const bannerViewOrders = document.getElementById('banner-view-orders');
const serviceShortcutGrid = document.getElementById('service-shortcut-grid');
const recentOrderCard = document.getElementById('recent-order-card');

// DOM Elements: Orders Desk & Toolbar
const refreshOrders = document.getElementById('refresh-orders');
const orderSearchInput = document.getElementById('order-search');
const clearSearchBtn = document.getElementById('clear-search');
const orderSortSelect = document.getElementById('order-sort');
const filterPills = document.querySelectorAll('.filter-pill');
const activityWeek = document.getElementById('activity-week');

// DOM Elements: Receipt Modal
const receiptModal = document.getElementById('receipt-modal');
const closeReceipt = document.getElementById('close-receipt');
const receiptContent = document.getElementById('receipt-content');

// State Variables
let isRegistering = false;
let currentAccount = null;
let currentServices = [];
let dashboardOrders = [];
let currentFilter = 'all';
let currentSearch = '';
let currentSort = 'newest';
let attachedFile = null;

const collectionPoints = [
    { name: 'Central Campus Counter', detail: 'Main Academic Building · Ground floor (West Wing)', hours: '08:00 – 18:00' },
    { name: 'Library Print Desk', detail: 'University Central Library · Level 1 Reprographics Section', hours: '08:30 – 20:00' },
    { name: 'Science Block Counter', detail: 'Science & Lab Complex · Ground Reception Desk', hours: '08:30 – 17:30' },
    { name: 'Airport Road Campus Counter', detail: 'Airport Road Campus · Gate 2 Reprographics Annex', hours: '08:00 – 19:00' },
];

const helpAnswers = {
    order: [
        'How do I place a print order?',
        'Drop your document into the Print Desk studio, select your required service (Black & White Xerox, Colour Print, Binding, etc.), set page count, pick a pickup counter, and click "Submit Print Request".'
    ],
    status: [
        'How do order status updates work?',
        'Orders transition smoothly through three stages: "Pending" (queued for processing), "Processing" (currently running on the machine), and "Completed" (ready at the counter for pickup).'
    ],
    document: [
        'What file types and page limits are accepted?',
        'We support standard PDF, Microsoft Word (DOC/DOCX), JPG, and PNG files up to 25MB per upload. All files are encrypted and processed securely.'
    ],
    contact: [
        'Where can I get counter or payment help?',
        'Visit the Central Campus Counter on the ground floor between 08:00 and 18:00, or speak with the reprographics operator on duty.'
    ],
};

// Utilities
function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>'"]/g, (char) => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    })[char]);
}

function money(value) {
    return `₹${Number(value || 0).toFixed(2)}`;
}

function statusBadgeClass(status) {
    if (status === 'Completed') return 'badge-completed';
    if (status === 'Processing') return 'badge-processing';
    return 'badge-pending';
}

function initials(name) {
    return String(name || 'Account')
        .split(/\s+/)
        .filter(Boolean)
        .slice(0, 2)
        .map((part) => part[0].toUpperCase())
        .join('');
}

function updateDashboardDate() {
    const now = new Date();
    const dateElement = document.getElementById('dashboard-date');
    if (dateElement) {
        dateElement.textContent = new Intl.DateTimeFormat(undefined, {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
            year: 'numeric',
        }).format(now);
        dateElement.dateTime = now.toISOString().split('T')[0];
    }
}
updateDashboardDate();
window.setInterval(updateDashboardDate, 60 * 1000);

// Authentication Logic
function updateAuthMode() {
    isRegistering = !isRegistering;
    nameField.hidden = !isRegistering;
    phoneField.hidden = !isRegistering;
    document.getElementById('name').required = isRegistering;
    document.getElementById('phone').required = false;

    authEyebrow.textContent = isRegistering ? 'NEW STUDENT REGISTRATION' : 'CAMPUS PRINTING PORTAL';
    authTitle.textContent = isRegistering ? 'Create your student account' : 'Welcome to your print desk';
    authSubtitle.textContent = isRegistering
        ? 'Register once to submit print jobs and track orders campus-wide.'
        : 'Sign in to place print orders, calculate rates, or track pickup progress.';
    authSubmit.innerHTML = isRegistering
        ? '<span>Create account</span> <span class="btn-arrow">&rarr;</span>'
        : '<span>Sign in</span> <span class="btn-arrow">&rarr;</span>';
    switchMode.textContent = isRegistering ? 'Sign in instead' : 'Create an account';
    formMessage.textContent = '';
}
switchMode.addEventListener('click', updateAuthMode);

// Forgot Password Dialog
if (forgotLink) {
    forgotLink.addEventListener('click', (e) => {
        e.preventDefault();
        forgotModal.hidden = false;
    });
}
if (closeForgot) closeForgot.addEventListener('click', () => { forgotModal.hidden = true; });
if (dismissForgot) dismissForgot.addEventListener('click', () => { forgotModal.hidden = true; });
if (forgotModal) {
    forgotModal.addEventListener('click', (e) => {
        if (e.target === forgotModal) forgotModal.hidden = true;
    });
}

// Authentication Submit
authForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const email = document.getElementById('email').value.trim().toLowerCase();
    const password = document.getElementById('password').value;
    authSubmit.disabled = true;
    formMessage.textContent = isRegistering ? 'Creating account...' : 'Signing in...';

    try {
        const endpoint = isRegistering ? '/api/register' : '/api/login';
        const body = isRegistering
            ? { name: document.getElementById('name').value.trim(), email, phone: document.getElementById('phone').value.trim(), password }
            : { email, password, role: roleInput.value };

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || (isRegistering ? 'Unable to create account.' : 'Unable to sign in.'));
        }
        currentAccount = result;
        await loadDashboard(result);
    } catch (error) {
        formMessage.textContent = error.message;
    } finally {
        authSubmit.disabled = false;
    }
});

// Tab Navigation Logic
function setView(tabName) {
    const tabs = document.querySelectorAll('.tab-pane');
    tabs.forEach((tab) => {
        const isMatch = tab.id === `tab-${tabName}`;
        tab.hidden = !isMatch;
        tab.classList.toggle('active', isMatch);
    });

    document.querySelectorAll('.nav-tab[data-tab]').forEach((btn) => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Attach Tab Listeners
document.querySelectorAll('.nav-tab[data-tab]').forEach((btn) => {
    btn.addEventListener('click', () => setView(btn.dataset.tab));
});

// Shortcut buttons between tabs
const viewOrdersShortcut = document.getElementById('view-orders-shortcut');
if (viewOrdersShortcut) viewOrdersShortcut.addEventListener('click', () => setView('orders'));

const allOrdersLink = document.getElementById('all-orders-link');
if (allOrdersLink) allOrdersLink.addEventListener('click', () => setView('orders'));

const seeAllServicesLink = document.getElementById('see-all-services-link');
if (seeAllServicesLink) seeAllServicesLink.addEventListener('click', () => setView('services'));

if (bannerViewOrders) bannerViewOrders.addEventListener('click', () => setView('orders'));

if (modalGoToDesk) {
    modalGoToDesk.addEventListener('click', () => {
        if (orderModal) orderModal.hidden = true;
        setView('print');
    });
}

if (addExpense) {
    addExpense.addEventListener('click', () => {
        setView('print');
        if (serviceSelect) serviceSelect.focus();
    });
}

// Stepper buttons for Copies / Pages
if (copiesMinus && copiesInput) {
    copiesMinus.addEventListener('click', () => {
        const current = parseInt(copiesInput.value, 10) || 1;
        copiesInput.value = Math.max(1, current - 1);
        updateLiveCostCalculation();
    });
}

if (copiesPlus && copiesInput) {
    copiesPlus.addEventListener('click', () => {
        const current = parseInt(copiesInput.value, 10) || 1;
        copiesInput.value = Math.min(1000, current + 1);
        updateLiveCostCalculation();
    });
}

// Role-Adapted Dashboard Loader
async function loadDashboard(account) {
    const response = await fetch('/api/dashboard');
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Unable to load dashboard.');

    currentAccount = account;
    currentServices = data.services || [];
    dashboardOrders = data.orders || [];

    const isStaff = account && account.role === 'staff';

    // 1. Role-Adaptive Navigation Configuration:
    // User requested: "the only my order details and activity treand should be in admin dashbord"
    const tabPrint = document.getElementById('tab-nav-print');
    const tabOrders = document.getElementById('tab-nav-orders');
    const tabActivity = document.getElementById('tab-nav-activity');
    const tabServices = document.getElementById('tab-nav-services');
    const tabCollection = document.getElementById('tab-nav-collection');
    const tabHelp = document.getElementById('tab-nav-help');

    if (isStaff) {
        // ADMIN DASHBOARD: ONLY Order Details & Activity Trends!
        if (tabPrint) tabPrint.hidden = true;
        if (tabServices) tabServices.hidden = true;
        if (tabCollection) tabCollection.hidden = true;
        if (tabHelp) tabHelp.hidden = true;

        if (tabOrders) tabOrders.hidden = false;
        if (tabActivity) tabActivity.hidden = false;

        if (appDeskTag) appDeskTag.textContent = 'Admin Dispatch Desk';
        if (navOrdersLabel) navOrdersLabel.textContent = 'All Order Details';

        const ordersEyebrow = document.getElementById('orders-eyebrow');
        if (ordersEyebrow) ordersEyebrow.textContent = 'CAMPUS REPROGRAPHICS DISPATCH';

        const ordersMainTitle = document.getElementById('orders-main-title');
        if (ordersMainTitle) ordersMainTitle.textContent = 'All Order Details & Processing';

        const expLabel = document.getElementById('expenditure-label');
        if (expLabel) expLabel.textContent = 'TOTAL REVENUE COLLECTED';

        if (addExpense) addExpense.hidden = true;

        // Admin immediately lands on All Order Details!
        setView('orders');
    } else {
        // STUDENT DASHBOARD: Print Desk, My Orders, Services, Collection, Help
        // Activity & Trends is an admin metric, so hide from student
        if (tabPrint) tabPrint.hidden = false;
        if (tabOrders) tabOrders.hidden = false;
        if (tabServices) tabServices.hidden = false;
        if (tabCollection) tabCollection.hidden = false;
        if (tabHelp) tabHelp.hidden = false;

        if (tabActivity) tabActivity.hidden = true;

        if (appDeskTag) appDeskTag.textContent = 'Student Portal';
        if (navOrdersLabel) navOrdersLabel.textContent = 'My Orders';

        const ordersEyebrow = document.getElementById('orders-eyebrow');
        if (ordersEyebrow) ordersEyebrow.textContent = 'ORDER MANAGEMENT';

        const ordersMainTitle = document.getElementById('orders-main-title');
        if (ordersMainTitle) ordersMainTitle.textContent = 'Your Print Orders & Requests';

        const expLabel = document.getElementById('expenditure-label');
        if (expLabel) expLabel.textContent = 'ESTIMATED EXPENDITURE';

        if (addExpense) addExpense.hidden = false;

        // Student immediately lands on clean Print Desk!
        setView('print');
    }

    document.getElementById('profile-avatar').textContent = initials(account.name);
    document.getElementById('profile-name').textContent = account.name;
    document.getElementById('profile-role').textContent = isStaff ? 'Desk Admin / Staff' : 'Student';
    document.getElementById('dashboard-title').innerHTML = `${isStaff ? 'Staff Dispatch Desk' : `Ready to print, ${escapeHtml(account.name)}`} <span>✦</span>`;

    renderDashboard(data);
    renderCollectionPoints();
    renderHelp();
    populateServiceSelect();
    renderServiceShortcuts();
    updateLiveCostCalculation();

    formMessage.textContent = '';
    authView.hidden = true;
    dashboardView.hidden = false;
    window.scrollTo(0, 0);
}

// Help Center Logic
function renderHelp() {
    document.querySelectorAll('.help-card').forEach((card) => {
        card.addEventListener('click', () => {
            const answer = helpAnswers[card.dataset.help];
            const answerPanel = document.getElementById('help-answer');
            if (answer && answerPanel) {
                answerPanel.innerHTML = `<strong>${escapeHtml(answer[0])}</strong><p>${escapeHtml(answer[1])}</p>`;
                answerPanel.hidden = false;
            }
        });
    });
}

// Collection Points Logic
function renderCollectionPoints() {
    const container = document.getElementById('collection-list');
    if (!container) return;
    container.innerHTML = collectionPoints.map((point, index) => `
        <div class="collection-hub-card">
            <div class="hub-header">
                <span class="hub-index">0${index + 1}</span>
                <span class="hub-status-pill">Active Counter</span>
            </div>
            <div class="hub-body">
                <strong>${escapeHtml(point.name)}</strong>
                <p class="hub-detail">${escapeHtml(point.detail)}</p>
                <div class="hub-meta">
                    <span class="hub-hours">🕒 ${escapeHtml(point.hours)}</span>
                </div>
            </div>
            <button type="button" class="hub-action-btn" data-collection="${escapeHtml(point.name)}">
                <span>Select for Next Print</span> &rarr;
            </button>
        </div>
    `).join('');

    container.querySelectorAll('.hub-action-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
            collectionSelect.value = btn.dataset.collection;
            setView('print');
            showToast(`Collection point set to ${btn.dataset.collection}`, 'info');
        });
    });
}

// Populate Service Select
function populateServiceSelect() {
    if (!currentServices.length) return;
    serviceSelect.innerHTML = currentServices.map((service) => `
        <option value="${service.service_id}" data-rate="${service.price_per_page}">
            ${escapeHtml(service.service_name)} (₹${Number(service.price_per_page).toFixed(2)} / page)
        </option>
    `).join('');
}

// Render Service Shortcuts on Print Desk
function renderServiceShortcuts() {
    if (!serviceShortcutGrid || !currentServices.length) return;

    const popularServices = currentServices.slice(0, 4);
    serviceShortcutGrid.innerHTML = popularServices.map((s, idx) => {
        const icons = ['📄', '🎨', '📚', '🔍'];
        return `
            <div class="service-shortcut-tile" data-service-id="${s.service_id}">
                <div class="tile-icon-box">${icons[idx % icons.length]}</div>
                <div class="tile-info">
                    <strong>${escapeHtml(s.service_name)}</strong>
                    <span class="tile-rate">${money(s.price_per_page)} / page</span>
                </div>
                <span class="tile-arrow">&plus;</span>
            </div>
        `;
    }).join('');

    serviceShortcutGrid.querySelectorAll('.service-shortcut-tile').forEach((tile) => {
        tile.addEventListener('click', () => {
            serviceSelect.value = tile.dataset.serviceId;
            updateLiveCostCalculation();
            copiesInput.focus();
            showToast(`Selected ${serviceSelect.options[serviceSelect.selectedIndex].text.split('(')[0].trim()}`, 'info');
        });
    });
}

// Live Cost Calculation
function updateLiveCostCalculation() {
    const selectedOption = serviceSelect.options[serviceSelect.selectedIndex];
    const rate = selectedOption ? parseFloat(selectedOption.dataset.rate || 0) : 2.0;
    const copies = Math.max(1, parseInt(copiesInput.value, 10) || 1);
    const total = rate * copies;

    if (calcRate) calcRate.textContent = money(rate);
    if (calcCopies) calcCopies.textContent = `${copies} ${copies === 1 ? 'page' : 'pages'}`;
    if (calcTotal) calcTotal.textContent = money(total);
}

if (serviceSelect) serviceSelect.addEventListener('change', updateLiveCostCalculation);
if (copiesInput) copiesInput.addEventListener('input', updateLiveCostCalculation);

// File Dropzone Handling
if (fileDropzone && orderFileInput) {
    fileDropzone.addEventListener('click', (e) => {
        if (e.target !== removeFileBtn) orderFileInput.click();
    });

    ['dragenter', 'dragover'].forEach((eventName) => {
        fileDropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            fileDropzone.classList.add('drag-active');
        });
    });

    ['dragleave', 'drop'].forEach((eventName) => {
        fileDropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            fileDropzone.classList.remove('drag-active');
        });
    });

    fileDropzone.addEventListener('drop', (e) => {
        if (e.dataTransfer.files.length) {
            handleSelectedFile(e.dataTransfer.files[0]);
        }
    });

    orderFileInput.addEventListener('change', () => {
        if (orderFileInput.files.length) {
            handleSelectedFile(orderFileInput.files[0]);
        }
    });
}

function handleSelectedFile(file) {
    attachedFile = file;
    dropzonePrompt.hidden = true;
    filePreview.hidden = false;
    previewFilename.textContent = file.name;
    const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);
    previewFilesize.textContent = `${sizeInMB} MB · Ready to print`;
}

if (removeFileBtn) {
    removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        attachedFile = null;
        orderFileInput.value = '';
        filePreview.hidden = true;
        dropzonePrompt.hidden = false;
    });
}

// Render Dashboard Data
function renderDashboard(data) {
    const summary = data.summary;
    dashboardOrders = data.orders || [];

    // Update KPI metrics on Orders tab
    document.getElementById('active-orders').textContent = `${summary.active_orders} in progress`;
    document.getElementById('active-orders-note').innerHTML = `${summary.pending_orders} pending, ${summary.processing_orders} processing`;
    document.getElementById('total-orders').textContent = `${summary.total_orders} order${summary.total_orders === 1 ? '' : 's'}`;
    document.getElementById('copies-total').textContent = `${summary.total_copies} total copies printed`;
    document.getElementById('order-value').textContent = money(summary.total_value);
    document.getElementById('completed-orders').textContent = `${summary.completed_orders} completed jobs`;
    document.getElementById('orders-heading').textContent = `${summary.total_orders} order${summary.total_orders === 1 ? '' : 's'} recorded`;

    // Update Navbar order badge
    if (navOrderCount) {
        if (dashboardOrders.length > 0) {
            navOrderCount.textContent = dashboardOrders.length;
            navOrderCount.hidden = false;
        } else {
            navOrderCount.hidden = true;
        }
    }

    // Active Job Banner on Print Desk (Only shown if user has active order)
    const activeOrder = dashboardOrders.find((o) => o.status === 'Pending' || o.status === 'Processing');
    if (activeJobBanner) {
        if (activeOrder) {
            activeJobTitle.textContent = `Order #XE-${activeOrder.order_id} is ${activeOrder.status}`;
            activeJobDesc.textContent = `${escapeHtml(activeOrder.service_name)} (${activeOrder.copies} copies) · Placed at ${escapeHtml(activeOrder.order_date || 'Today')}`;
            activeJobBanner.hidden = false;
        } else {
            activeJobBanner.hidden = true;
        }
    }

    // Recent Order Card on Print Desk
    if (recentOrderCard) {
        if (dashboardOrders.length > 0) {
            const latest = dashboardOrders[0];
            recentOrderCard.innerHTML = `
                <div class="recent-card-left">
                    <span class="recent-token">#XE-${latest.order_id}</span>
                    <div class="recent-info">
                        <strong>${escapeHtml(latest.service_name)}</strong>
                        <small>${latest.copies} ${latest.copies === 1 ? 'page' : 'pages'} · Total ${money(latest.total)}</small>
                    </div>
                </div>
                <div class="recent-card-right">
                    <span class="status-chip ${statusBadgeClass(latest.status)}"><span class="chip-dot"></span>${escapeHtml(latest.status)}</span>
                    <button type="button" class="btn-receipt-sm" data-order-id="${latest.order_id}">Receipt &rarr;</button>
                </div>
            `;
            const receiptSmBtn = recentOrderCard.querySelector('.btn-receipt-sm');
            if (receiptSmBtn) {
                receiptSmBtn.addEventListener('click', () => showOrderReceipt(latest.order_id));
            }
        } else {
            recentOrderCard.innerHTML = `<p class="empty-state">No print jobs placed yet. Upload your first document above!</p>`;
        }
    }

    // Services Catalogue on Services Tab
    const servicesListContainer = document.getElementById('services-list');
    if (servicesListContainer) {
        servicesListContainer.innerHTML = data.services.length
            ? data.services.map((service, index) => `
                <div class="catalogue-item-card" data-service-id="${service.service_id}">
                    <div class="catalogue-icon-wrap">${['📄', '🎨', '📚', '🔍', '📑'][index % 5]}</div>
                    <div class="catalogue-body">
                        <strong>${escapeHtml(service.service_name)}</strong>
                        <p class="catalogue-rate">${money(service.price_per_page)} <small>/ page (A4 80 GSM)</small></p>
                        <span class="catalogue-tag">Standard Campus Spec</span>
                    </div>
                    <button type="button" class="primary-button btn-sm catalogue-select-btn">
                        <span>Print with this &rarr;</span>
                    </button>
                </div>
            `).join('')
            : '<p class="empty-state">No services are available.</p>';

        servicesListContainer.querySelectorAll('.catalogue-select-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                const card = e.target.closest('.catalogue-item-card');
                serviceSelect.value = card.dataset.serviceId;
                updateLiveCostCalculation();
                setView('print');
                copiesInput.focus();
            });
        });
    }

    renderOrdersTable();
    renderWeeklyActivity(dashboardOrders);
    renderNotificationsDrawer(dashboardOrders);
}

// Orders Filter, Search & Sort Logic
function filterAndSortOrders() {
    let result = [...dashboardOrders];

    // Status Filter
    if (currentFilter !== 'all') {
        result = result.filter((o) => o.status === currentFilter);
    }

    // Search Filter
    if (currentSearch.trim()) {
        const query = currentSearch.trim().toLowerCase();
        result = result.filter((o) => {
            const idMatch = `#xe-${o.order_id}`.toLowerCase().includes(query) || String(o.order_id).includes(query);
            const studentMatch = (o.student_name || '').toLowerCase().includes(query);
            const serviceMatch = (o.service_name || '').toLowerCase().includes(query);
            return idMatch || studentMatch || serviceMatch;
        });
    }

    // Sorting
    result.sort((a, b) => {
        if (currentSort === 'newest') return (parseOrderDate(b.order_date) || 0) - (parseOrderDate(a.order_date) || 0);
        if (currentSort === 'oldest') return (parseOrderDate(a.order_date) || 0) - (parseOrderDate(b.order_date) || 0);
        if (currentSort === 'copies-desc') return b.copies - a.copies;
        if (currentSort === 'copies-asc') return a.copies - b.copies;
        if (currentSort === 'total-desc') return b.total - a.total;
        if (currentSort === 'id-asc') return a.order_id - b.order_id;
        return 0;
    });

    return result;
}

function renderOrdersTable() {
    const listContainer = document.getElementById('orders-list');
    const filtered = filterAndSortOrders();

    if (!filtered.length) {
        if (!dashboardOrders.length) {
            listContainer.innerHTML = '<p class="empty-state">No orders yet.</p>';
            return;
        }

        listContainer.innerHTML = `
            <div class="empty-search-state">
                <span class="empty-icon">🔍</span>
                <p>No orders match the current filter or search criteria.</p>
                <button type="button" class="text-button" id="reset-filters">Clear all filters</button>
            </div>
        `;
        const resetBtn = document.getElementById('reset-filters');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                currentFilter = 'all';
                currentSearch = '';
                orderSearchInput.value = '';
                clearSearchBtn.hidden = true;
                filterPills.forEach((p) => p.classList.toggle('active', p.dataset.filter === 'all'));
                renderOrdersTable();
            });
        }
        return;
    }

    listContainer.innerHTML = filtered.map((order) => {
        const isStaff = currentAccount && currentAccount.role === 'staff';
        const statusControl = isStaff
            ? `<select class="order-status-select ${statusBadgeClass(order.status)}" data-order-id="${order.order_id}" aria-label="Update status for order ${order.order_id}">
                    <option value="Pending" ${order.status === 'Pending' ? 'selected' : ''}>Pending</option>
                    <option value="Processing" ${order.status === 'Processing' ? 'selected' : ''}>Processing</option>
                    <option value="Completed" ${order.status === 'Completed' ? 'selected' : ''}>Completed</option>
               </select>`
            : `<span class="status-chip ${statusBadgeClass(order.status)}"><span class="chip-dot"></span>${escapeHtml(order.status)}</span>`;

        return `
            <div class="order-row" data-order-id="${order.order_id}">
                <span class="order-id">#XE-${order.order_id}</span>
                <span class="order-student">${escapeHtml(order.student_name || 'You')}</span>
                <span class="order-service">${escapeHtml(order.service_name)}</span>
                <span class="order-copies">${order.copies} ${order.copies === 1 ? 'page' : 'pages'}</span>
                <span class="order-status-col">${statusControl}</span>
                <strong class="order-total">${money(order.total)}</strong>
                <span class="order-actions">
                    <button type="button" class="btn-receipt" data-order-id="${order.order_id}" title="View order receipt">Receipt &rarr;</button>
                    ${!isStaff ? `<button type="button" class="btn-delete-order" data-order-id="${order.order_id}" aria-label="Delete order ${order.order_id}">Delete</button>` : ''}
                </span>
            </div>
        `;
    }).join('');

    // Status change listener for staff
    listContainer.querySelectorAll('.order-status-select').forEach((select) => {
        select.addEventListener('change', (e) => {
            e.stopPropagation();
            updateOrderStatus(select.dataset.orderId, select.value);
        });
    });

    // Receipt click listener
    listContainer.querySelectorAll('.btn-receipt, .order-id').forEach((el) => {
        el.addEventListener('click', (e) => {
            e.stopPropagation();
            const orderId = parseInt(el.dataset.orderId || el.closest('.order-row').dataset.orderId, 10);
            showOrderReceipt(orderId);
        });
    });

    listContainer.querySelectorAll('.btn-delete-order').forEach((button) => {
        button.addEventListener('click', () => deleteOrder(button.dataset.orderId, button));
    });
}

// Search and Filter Toolbar Listeners
if (orderSearchInput) {
    orderSearchInput.addEventListener('input', () => {
        currentSearch = orderSearchInput.value;
        clearSearchBtn.hidden = !currentSearch.length;
        renderOrdersTable();
    });
}

if (clearSearchBtn) {
    clearSearchBtn.addEventListener('click', () => {
        orderSearchInput.value = '';
        currentSearch = '';
        clearSearchBtn.hidden = true;
        renderOrdersTable();
        orderSearchInput.focus();
    });
}

filterPills.forEach((pill) => {
    pill.addEventListener('click', () => {
        filterPills.forEach((p) => p.classList.remove('active'));
        pill.classList.add('active');
        currentFilter = pill.dataset.filter;
        renderOrdersTable();
    });
});

if (orderSortSelect) {
    orderSortSelect.addEventListener('change', () => {
        currentSort = orderSortSelect.value;
        renderOrdersTable();
    });
}

// Receipt Modal View
function showOrderReceipt(orderId) {
    const order = dashboardOrders.find((o) => o.order_id === orderId);
    if (!order) return;

    receiptContent.innerHTML = `
        <div class="receipt-header">
            <span class="brand-mark">x</span>
            <div>
                <h3>XeroEasy Campus Reprographics</h3>
                <small>Order Token: #XE-${order.order_id}</small>
            </div>
        </div>
        <div class="receipt-body">
            <div class="receipt-row"><span>Student Name:</span><strong>${escapeHtml(order.student_name || 'Current Student')}</strong></div>
            <div class="receipt-row"><span>Service Type:</span><strong>${escapeHtml(order.service_name)}</strong></div>
            <div class="receipt-row"><span>Price per Page:</span><span>${money(order.price_per_page)}</span></div>
            <div class="receipt-row"><span>Copies / Pages:</span><span>${order.copies}</span></div>
            <div class="receipt-row"><span>Order Placed:</span><span>${escapeHtml(order.order_date || 'Today')}</span></div>
            <div class="receipt-row"><span>Pickup Counter:</span><strong>${escapeHtml(collectionSelect ? collectionSelect.value : 'Central Campus Counter')}</strong></div>
            <div class="receipt-divider"></div>
            <div class="receipt-total-row"><span>Total Amount Paid:</span><strong>${money(order.total)}</strong></div>
            <div class="receipt-status-box ${statusBadgeClass(order.status)}">
                <span>Current Status:</span>
                <strong>${escapeHtml(order.status)}</strong>
            </div>
        </div>
        <div class="receipt-actions">
            <button type="button" class="primary-button" id="btn-download-receipt">
                <span>Download Receipt</span>
                <span class="btn-arrow">📥</span>
            </button>
        </div>
    `;

    const btnDownload = receiptContent.querySelector('#btn-download-receipt');
    if (btnDownload) {
        btnDownload.addEventListener('click', () => {
            downloadReceipt(order);
        });
    }

    receiptModal.hidden = false;
}

// Download Receipt Handler
function downloadReceipt(order) {
    const pickupCounter = collectionSelect ? collectionSelect.value : 'Central Campus Counter';
    const content = `====================================================
               XEROEASY REPROGRAPHICS
           Smart Campus Reprographics Desk
====================================================
OFFICIAL RECEIPT & AUDIT TOKEN

Receipt ID     : #XE-${order.order_id}
Order Date     : ${order.order_date || new Date().toLocaleString()}
Student Name   : ${order.student_name || (currentAccount ? currentAccount.name : 'Student')}
Account Email  : ${currentAccount ? currentAccount.email : 'student@college.edu'}

SERVICE DETAILS
----------------------------------------------------
Service Type   : ${order.service_name}
Rate / Page    : ₹${Number(order.price_per_page || 0).toFixed(2)}
Copies / Pages : ${order.copies}
Paper Standard : A4 80 GSM Bond Paper
Pickup Counter : ${pickupCounter}
Order Status   : ${order.status}

BILLING BREAKDOWN
----------------------------------------------------
Base Subtotal  : ₹${Number(order.total || 0).toFixed(2)}
Taxes & Duties : ₹0.00 (Campus Subsidized)
====================================================
TOTAL AMOUNT   : ₹${Number(order.total || 0).toFixed(2)}
====================================================

COLLECTION INSTRUCTIONS:
1. Present this order token (#XE-${order.order_id}) at ${pickupCounter}.
2. Verify printed pages before leaving the counter.
3. Reprographics Support: support@xeroeasy.local

Thank you for using XeroEasy Campus Reprographics!
====================================================`;

    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `XeroEasy_Receipt_XE-${order.order_id}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    showToast(`Receipt #XE-${order.order_id} downloaded successfully!`, 'success');
}

if (closeReceipt) closeReceipt.addEventListener('click', () => { receiptModal.hidden = true; });
if (receiptModal) {
    receiptModal.addEventListener('click', (e) => {
        if (e.target === receiptModal) receiptModal.hidden = true;
    });
}

// Notifications Drawer
function renderNotificationsDrawer(orders) {
    if (!notificationsList) return;
    const completed = orders.filter((o) => o.status === 'Completed').slice(0, 3);
    const inProgress = orders.filter((o) => o.status === 'Processing').slice(0, 2);

    let html = '';
    if (completed.length) {
        completed.forEach((o) => {
            html += `
                <div class="notify-card notify-success">
                    <span class="notify-icon">✓</span>
                    <div>
                        <strong>Order #XE-${o.order_id} is Ready!</strong>
                        <p>Your ${escapeHtml(o.service_name)} (${o.copies} copies) is printed and ready at the counter.</p>
                        <small>${escapeHtml(o.order_date || 'Just now')}</small>
                    </div>
                </div>
            `;
        });
    }
    if (inProgress.length) {
        inProgress.forEach((o) => {
            html += `
                <div class="notify-card notify-info">
                    <span class="notify-icon">⚙</span>
                    <div>
                        <strong>Order #XE-${o.order_id} is Printing</strong>
                        <p>The reprographics operator is currently processing your document.</p>
                    </div>
                </div>
            `;
        });
    }
    if (!html) {
        html = `
            <div class="empty-state" style="text-align:center; padding: 30px 10px;">
                <p>No new notifications. All orders are up to date!</p>
            </div>
        `;
    }
    notificationsList.innerHTML = html;
}

if (btnNotifications) {
    btnNotifications.addEventListener('click', () => {
        notificationsModal.hidden = false;
    });
}
if (closeNotifications) {
    closeNotifications.addEventListener('click', () => {
        notificationsModal.hidden = true;
    });
}
if (notificationsModal) {
    notificationsModal.addEventListener('click', (e) => {
        if (e.target === notificationsModal) notificationsModal.hidden = true;
    });
}

// Status Updates (Staff)
async function updateOrderStatus(orderId, status) {
    try {
        const response = await fetch(`/api/orders/${orderId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status }),
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Could not update order status.');

        if (result.email_notification === 'sent') {
            showToast(`Order #XE-${orderId} marked ${status}. Student alert email sent!`, 'success');
        } else {
            showToast(`Order #XE-${orderId} updated to ${status}.`, 'info');
        }
        await reloadDashboard();
    } catch (error) {
        alert(error.message);
    }
}

async function deleteOrder(orderId, button) {
    if (!window.confirm(`Delete order #XE-${orderId}? You can undo this from the confirmation message.`)) return;

    button.disabled = true;
    try {
        const response = await fetch(`/api/orders/${orderId}`, { method: 'DELETE' });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Could not delete the order.');

        showToast(`Order #XE-${orderId} deleted.`, 'success', {
            label: 'Undo',
            onClick: (toast, undoButton) => restoreOrder(orderId, toast, undoButton),
        });
        await reloadDashboard();
    } catch (error) {
        alert(error.message);
    } finally {
        button.disabled = false;
    }
}

async function restoreOrder(orderId, toast, undoButton) {
    undoButton.disabled = true;
    try {
        const response = await fetch(`/api/orders/${orderId}/restore`, { method: 'POST' });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Could not restore the order.');

        toast.remove();
        showToast(`Order #XE-${orderId} restored.`, 'success');
        try {
            await reloadDashboard();
        } catch (error) {
            alert(`Order restored, but the dashboard could not be refreshed: ${error.message}`);
        }
    } catch (error) {
        undoButton.disabled = false;
        alert(error.message);
    }
}

function showToast(message, type = 'info', action = null) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const text = document.createElement('span');
    text.textContent = message;
    toast.appendChild(text);
    if (action) {
        const actionButton = document.createElement('button');
        actionButton.type = 'button';
        actionButton.className = 'toast-action';
        actionButton.textContent = action.label;
        actionButton.addEventListener('click', () => action.onClick(toast, actionButton));
        toast.appendChild(actionButton);
    }
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('toast-visible');
    }, 50);
    setTimeout(() => {
        toast.classList.remove('toast-visible');
        setTimeout(() => toast.remove(), 300);
    }, action ? 8000 : 3500);
}

// Reload Dashboard
async function reloadDashboard() {
    const response = await fetch('/api/dashboard', { cache: 'no-store' });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Could not refresh the dashboard.');
    renderDashboard(data);
}

// Sign Out
signOut.addEventListener('click', async () => {
    signOut.disabled = true;
    try {
        const response = await fetch('/api/logout', { method: 'POST' });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Could not sign out.');
        dashboardView.hidden = true;
        authView.hidden = false;
        authForm.reset();
        if (isRegistering) updateAuthMode();
    } catch (error) {
        alert(error.message);
    } finally {
        signOut.disabled = false;
    }
});

// Order Creation Submit
orderForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const submitBtn = document.getElementById('btn-submit-order');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Submitting order...</span>';

    try {
        const response = await fetch('/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                service_id: serviceSelect.value,
                copies: copiesInput.value,
            }),
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Could not create order.');

        showToast(`Order #XE-${result.order_id} successfully placed!`, 'success');

        // Reset file attachment
        attachedFile = null;
        if (orderFileInput) orderFileInput.value = '';
        if (filePreview) filePreview.hidden = true;
        if (dropzonePrompt) dropzonePrompt.hidden = false;

        // Reset copies
        copiesInput.value = 1;
        updateLiveCostCalculation();

        await reloadDashboard();
    } catch (error) {
        alert(error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<span>Submit Print Request</span> <span class="btn-arrow">&rarr;</span>';
    }
});

// Refresh Button Listener
refreshOrders.addEventListener('click', async () => {
    if (refreshOrders.disabled) return;
    const originalText = refreshOrders.innerHTML;
    refreshOrders.disabled = true;
    refreshOrders.setAttribute('aria-busy', 'true');
    refreshOrders.innerHTML = '<span>Refreshing…</span>';
    try {
        await reloadDashboard();
        showToast('Orders refreshed from MySQL database.', 'info');
    } catch (error) {
        alert(error.message);
    } finally {
        refreshOrders.disabled = false;
        refreshOrders.removeAttribute('aria-busy');
        refreshOrders.innerHTML = originalText;
    }
});

// Spline Chart Parsing
function parseOrderDate(value) {
    if (typeof value !== 'string' || !value) return null;
    const date = new Date(value.replace(' ', 'T'));
    return Number.isNaN(date.getTime()) ? null : date;
}

function startOfWeek(date) {
    const start = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    const dayFromMonday = (start.getDay() + 6) % 7;
    start.setDate(start.getDate() - dayFromMonday);
    return start;
}

function dateKey(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

function formatWeek(start) {
    const end = new Date(start);
    end.setDate(end.getDate() + 6);
    const format = new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric' });
    return `${format.format(start)} – ${format.format(end)}`;
}

function renderWeeklyActivity(orders) {
    if (!activityWeek) return;
    const previousWeek = activityWeek.value;
    const dates = orders.map((order) => parseOrderDate(order.order_date)).filter(Boolean);
    const currentWeek = startOfWeek(new Date());
    let firstWeek = dates.length ? startOfWeek(dates.reduce((earliest, date) => date < earliest ? date : earliest)) : currentWeek;
    const lastWeek = dates.length ? startOfWeek(dates.reduce((latest, date) => date > latest ? date : latest)) : currentWeek;
    if (firstWeek > currentWeek) firstWeek = currentWeek;
    const finalWeek = lastWeek > currentWeek ? lastWeek : currentWeek;
    const weeks = [];

    for (const week = new Date(firstWeek); week <= finalWeek; week.setDate(week.getDate() + 7)) {
        weeks.push(new Date(week));
    }

    activityWeek.replaceChildren(...weeks.map((week) => {
        const option = document.createElement('option');
        option.value = dateKey(week);
        option.textContent = `${dateKey(week) === dateKey(currentWeek) ? 'This week · ' : ''}${formatWeek(week)}`;
        return option;
    }));
    activityWeek.value = weeks.some((week) => dateKey(week) === previousWeek) ? previousWeek : dateKey(currentWeek);

    const selectedWeek = new Date(`${activityWeek.value}T00:00:00`);
    const followingWeek = new Date(selectedWeek);
    followingWeek.setDate(followingWeek.getDate() + 7);
    const counts = Array(7).fill(0);
    for (const date of dates) {
        if (date >= selectedWeek && date < followingWeek) {
            const dayIndex = (date.getDay() + 6) % 7;
            counts[dayIndex] += 1;
        }
    }

    const maxCount = Math.max(...counts);
    const axisMaximum = Math.max(4, Math.ceil(maxCount / 4) * 4);
    const axisElem = document.getElementById('activity-axis');
    const daysElem = document.getElementById('activity-days');
    if (axisElem) {
        axisElem.replaceChildren(
            ...Array.from({ length: 5 }, (_, index) => {
                const label = document.createElement('span');
                label.textContent = String(axisMaximum - (axisMaximum / 4) * index);
                return label;
            })
        );
    }
    if (daysElem) {
        daysElem.replaceChildren(
            ...['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day) => {
                const label = document.createElement('span');
                label.textContent = day;
                return label;
            })
        );
    }

    const points = counts.map((count, index) => ({
        x: (700 / 6) * index,
        y: 190 - (count / axisMaximum) * 170,
    }));
    let linePath = `M ${points[0].x} ${points[0].y}`;
    for (let index = 1; index < points.length; index += 1) {
        const previous = points[index - 1];
        const point = points[index];
        const midpointX = (previous.x + point.x) / 2;
        const midpointY = (previous.y + point.y) / 2;
        linePath += ` Q ${previous.x} ${previous.y} ${midpointX} ${midpointY}`;
        if (index === points.length - 1) linePath += ` T ${point.x} ${point.y}`;
    }
    const actLine = document.getElementById('activity-line');
    const actFill = document.getElementById('activity-fill');
    if (actLine) actLine.setAttribute('d', linePath);
    if (actFill) actFill.setAttribute('d', `${linePath} L 700 205 L 0 205 Z`);

    const weekTitle = dateKey(selectedWeek) === dateKey(currentWeek) ? 'Weekly Print Volume' : `Print Volume · ${formatWeek(selectedWeek)}`;
    const titleElem = document.getElementById('activity-title');
    if (titleElem) titleElem.textContent = weekTitle;
    const total = counts.reduce((sum, count) => sum + count, 0);
    const descElem = document.getElementById('activity-description');
    if (descElem) descElem.textContent = `${total} ${total === 1 ? 'order' : 'orders'} processed during ${formatWeek(selectedWeek)}.`;
}

if (activityWeek) {
    activityWeek.addEventListener('change', () => {
        renderWeeklyActivity(dashboardOrders);
    });
}
