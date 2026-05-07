{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Dashboard | Buildimity</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <meta name="csrf-token" content="{{ csrf_token }}">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0b0f19 100%);
            min-height: 100vh;
            color: #e2e8f0;
        }

        /* Top Navigation */
        .top-nav {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(12px);
            padding: 14px 24px;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }

        .logo h1 {
            font-size: 1.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .logo p {
            font-size: 0.7rem;
            color: #94a3b8;
        }

        .nav-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .btn {
            padding: 6px 16px;
            border-radius: 10px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border: none;
        }

        .btn-primary {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        }

        .btn-outline {
            background: rgba(255,255,255,0.1);
            color: white;
            border: 1px solid rgba(255,255,255,0.2);
        }

        .btn-outline:hover {
            background: rgba(255,255,255,0.2);
        }

        .btn-sm {
            padding: 4px 10px;
            font-size: 0.7rem;
        }

        .btn-success {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
        }

        .btn-danger {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
        }

        .btn-warning {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
        }

        /* Main Container */
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px 24px;
        }

        /* Welcome Banner - Compact */
        .welcome-banner {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.2), rgba(124, 58, 237, 0.2));
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px 24px;
            margin-bottom: 24px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .welcome-banner h2 {
            font-size: 1.3rem;
            margin-bottom: 4px;
        }

        .welcome-banner p {
            color: #94a3b8;
            font-size: 0.85rem;
            margin-bottom: 16px;
        }

        .stats-row {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        .stat-item {
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 12px 20px;
            min-width: 100px;
        }

        .stat-item .value {
            font-size: 1.5rem;
            font-weight: 700;
        }

        .stat-item .label {
            font-size: 0.7rem;
            color: #94a3b8;
        }

        /* Search Bar - Compact */
        .search-card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 16px 20px;
            margin-bottom: 24px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .search-card h3 {
            font-size: 1rem;
            margin-bottom: 4px;
        }

        .search-card p {
            color: #94a3b8;
            font-size: 0.75rem;
            margin-bottom: 12px;
        }

        .search-form {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .search-form input {
            flex: 1;
            padding: 10px 16px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            font-size: 0.85rem;
            color: white;
        }

        .search-form input:focus {
            outline: none;
            border-color: #2563eb;
        }

        .search-form button {
            padding: 10px 20px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.85rem;
        }

        /* Tab Navigation */
        .tabs {
            display: flex;
            gap: 4px;
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 4px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .tab-btn {
            padding: 10px 24px;
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            border-radius: 10px;
            transition: all 0.2s;
        }

        .tab-btn.active {
            background: rgba(37, 99, 235, 0.3);
            color: white;
        }

        .tab-btn:hover:not(.active) {
            background: rgba(255,255,255,0.1);
            color: white;
        }

        /* Tab Content */
        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* List Items - Compact */
        .list-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            margin-bottom: 8px;
            transition: all 0.2s;
            flex-wrap: wrap;
            gap: 10px;
        }

        .list-item:hover {
            background: rgba(255,255,255,0.08);
        }

        .item-info {
            flex: 2;
            min-width: 200px;
        }

        .item-title {
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 2px;
        }

        .item-meta {
            font-size: 0.7rem;
            color: #94a3b8;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        .item-status {
            min-width: 90px;
        }

        .badge {
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.65rem;
            font-weight: 600;
        }

        .badge-pending { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
        .badge-accepted { background: rgba(37, 99, 235, 0.2); color: #60a5fa; }
        .badge-paid { background: rgba(16, 185, 129, 0.2); color: #34d399; }
        .badge-in_progress { background: rgba(139, 92, 246, 0.2); color: #a78bfa; }
        .badge-completed { background: rgba(16, 185, 129, 0.2); color: #34d399; }
        .badge-negotiating { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
        .badge-open { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }

        .item-actions {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }

        /* Sidebar - Compact */
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .sidebar-card {
            background: rgba(255,255,255,0.03);
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.08);
            overflow: hidden;
        }

        .sidebar-header {
            padding: 12px 16px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            font-weight: 600;
            font-size: 0.85rem;
        }

        .sidebar-item {
            padding: 10px 16px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            display: flex;
            justify-content: space-between;
            align-items: center;
            text-decoration: none;
            color: #cbd5e1;
            font-size: 0.8rem;
            transition: all 0.2s;
        }

        .sidebar-item:hover {
            background: rgba(255,255,255,0.05);
            color: white;
        }

        .sidebar-item:last-child {
            border-bottom: none;
        }

        /* Two Column Layout */
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 280px;
            gap: 20px;
        }

        @media (max-width: 900px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 30px 20px;
            color: #64748b;
            font-size: 0.85rem;
        }

        /* Alert */
        .alert {
            background: rgba(37, 99, 235, 0.2);
            border-left: 3px solid #2563eb;
            padding: 10px 16px;
            border-radius: 10px;
            margin-bottom: 16px;
            font-size: 0.8rem;
        }

        /* Section Title */
        .section-title {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #64748b;
            margin-bottom: 12px;
        }
    </style>
</head>
<body>

    <!-- Top Navigation -->
    <nav class="top-nav">
        <div class="nav-container">
            <div class="logo">
                <h1><i class="fas fa-handshake"></i> Buildimity</h1>
                <p>Welcome, {{ user.username }}</p>
            </div>
            <div class="nav-buttons">
                {% if user.role == 'client' %}
                    <a href="{% url 'create_service_need' %}" class="btn btn-primary">
                        <i class="fas fa-plus-circle"></i> Request
                    </a>
                {% endif %}
                {% if user.role == 'provider' %}
                    <a href="{% url 'upload_work_image' %}" class="btn btn-primary">
                        <i class="fas fa-camera"></i> Upload
                    </a>
                    <a href="{% url 'provider_profile' %}" class="btn btn-outline">
                        <i class="fas fa-user-edit"></i> Profile
                    </a>
                {% endif %}
                <form action="{% url 'logout' %}" method="post" style="display: inline;">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-outline">
                        <i class="fas fa-sign-out-alt"></i> Logout
                    </button>
                </form>
            </div>
        </div>
    </nav>

    <main class="main-container">
        {% if messages %}
            {% for message in messages %}
                <div class="alert">
                    <i class="fas fa-info-circle"></i> {{ message }}
                </div>
            {% endfor %}
        {% endif %}

        <!-- ==================== CLIENT DASHBOARD ==================== -->
        {% if user.role == 'client' %}

            <!-- Welcome Banner -->
            <div class="welcome-banner">
                <div class="stats-row">
                    <div class="stat-item">
                        <div class="value">{{ total_requests|default:0 }}</div>
                        <div class="label">Total</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">{{ accepted_requests|default:0 }}</div>
                        <div class="label">Active</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">{{ completed_requests|default:0 }}</div>
                        <div class="label">Completed</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">UGX {{ total_spent|default:0|floatformat:0 }}</div>
                        <div class="label">Spent</div>
                    </div>
                </div>
            </div>

            <!-- Search Bar -->
            <div class="search-card">
                <form action="{% url 'client_search' %}" method="get" class="search-form">
                    <input type="text" name="q" placeholder="Search for a service..." value="{{ request.GET.q }}">
                    <button type="submit"><i class="fas fa-search"></i> Search</button>
                </form>
            </div>

            <div class="dashboard-grid">
                <!-- Main Content -->
                <div>
                    <!-- Tabs -->
                    <div class="tabs">
                        <button class="tab-btn active" onclick="showTab('requests')">
                            <i class="fas fa-comments"></i> Requests
                        </button>
                        <button class="tab-btn" onclick="showTab('needs')">
                            <i class="fas fa-list-alt"></i> Service Needs
                        </button>
                        <button class="tab-btn" onclick="showTab('payments')">
                            <i class="fas fa-credit-card"></i> Payments
                        </button>
                    </div>

                    <!-- Active Requests Tab -->
                    <div id="requests-tab" class="tab-content active">
                        <div class="section-title"><i class="fas fa-clock"></i> ACTIVE REQUESTS</div>
                        {% if requests %}
                            {% for req in requests %}
                            <div class="list-item">
                                <div class="item-info">
                                    <div class="item-title">{{ req.service_need.service_display|default:req.service.name }}</div>
                                    <div class="item-meta">
                                        <span><i class="fas fa-user"></i> {{ req.provider.username }}</span>
                                        <span><i class="fas fa-calendar"></i> {{ req.created_at|date:"M d" }}</span>
                                        <span><i class="fas fa-money-bill"></i> UGX {{ req.amount|floatformat:0 }}</span>
                                    </div>
                                </div>
                                <div class="item-status">
                                    <span class="badge badge-{{ req.status }}">{{ req.status }}</span>
                                </div>
                                <div class="item-actions">
                                    <a href="{% url 'service_request_detail' req.id %}" class="btn btn-outline btn-sm">View</a>
                                    {% if req.status == 'accepted' %}
                                        <a href="{% url 'make_payment' req.id %}" class="btn btn-success btn-sm">Pay</a>
                                    {% endif %}
                                    {% if req.status == 'in_progress' %}
                                        <a href="{% url 'confirm_completion' req.id %}" class="btn btn-warning btn-sm">Complete</a>
                                    {% endif %}
                                </div>
                            </div>
                            {% endfor %}
                        {% else %}
                            <div class="empty-state">No active requests</div>
                        {% endif %}
                    </div>

                    <!-- Service Needs Tab -->
                    <div id="needs-tab" class="tab-content">
                        <div class="section-title"><i class="fas fa-plus-circle"></i> RECENT NEEDS</div>
                        {% if needs %}
                            {% for need in needs %}
                            <div class="list-item">
                                <div class="item-info">
                                    <div class="item-title">
                                        {% if need.service %}{{ need.service.name }}{% elif need.custom_service_name %}{{ need.custom_service_name }}{% else %}Service Need{% endif %}
                                    </div>
                                    <div class="item-meta">
                                        <span><i class="fas fa-map-marker-alt"></i> {{ need.location|default:"Anywhere" }}</span>
                                        <span><i class="fas fa-calendar"></i> {{ need.created_at|date:"M d" }}</span>
                                    </div>
                                </div>
                                <div class="item-status">
                                    <span class="badge badge-{{ need.status|default:'open' }}">{{ need.status|default:"Open" }}</span>
                                </div>
                                <div class="item-actions">
                                    <a href="{% url 'match_providers' need.id %}" class="btn btn-primary btn-sm">Find Providers</a>
                                </div>
                            </div>
                            {% endfor %}
                        {% else %}
                            <div class="empty-state">No service needs yet. <a href="{% url 'create_service_need' %}">Create one</a></div>
                        {% endif %}
                        <div style="margin-top: 12px; text-align: center;">
                            <a href="{% url 'create_service_need' %}" class="btn btn-primary btn-sm">+ New Service Need</a>
                        </div>
                    </div>

                    <!-- Payments Tab -->
                    <div id="payments-tab" class="tab-content">
                        <div class="section-title"><i class="fas fa-history"></i> PAYMENT HISTORY</div>
                        {% if payments %}
                            {% for payment in payments %}
                            <div class="list-item">
                                <div class="item-info">
                                    <div class="item-title">Request #{{ payment.service_request.id }}</div>
                                    <div class="item-meta">
                                        <span><i class="fas fa-user"></i> {{ payment.provider.username }}</span>
                                        <span><i class="fas fa-calendar"></i> {{ payment.created_at|date:"M d, Y" }}</span>
                                    </div>
                                </div>
                                <div class="item-status">
                                    <span class="badge badge-{{ payment.status }}">{{ payment.status }}</span>
                                </div>
                                <div class="item-actions">
                                    <span class="btn btn-outline btn-sm disabled">UGX {{ payment.amount|floatformat:0 }}</span>
                                </div>
                            </div>
                            {% endfor %}
                        {% else %}
                            <div class="empty-state">No payment history</div>
                        {% endif %}
                    </div>
                </div>

                <!-- Sidebar -->
                <div class="sidebar">
                    <div class="sidebar-card">
                        <div class="sidebar-header"><i class="fas fa-bolt"></i> Quick Actions</div>
                        <a href="{% url 'create_service_need' %}" class="sidebar-item">
                            <span><i class="fas fa-plus-circle"></i> Post a Need</span>
                            <i class="fas fa-arrow-right"></i>
                        </a>
                        <a href="javascript:void(0)" onclick="updateUserLocation()" class="sidebar-item">
                            <span><i class="fas fa-location-dot"></i> Update Location</span>
                            <i class="fas fa-arrow-right"></i>
                        </a>
                        <a href="{% url 'my_favorites' %}" class="sidebar-item">
                            <span><i class="fas fa-heart"></i> Favorites</span>
                            <i class="fas fa-arrow-right"></i>
                        </a>
                        <a href="{% url 'notification_center' %}" class="sidebar-item">
                            <span><i class="fas fa-bell"></i> Notifications</span>
                            <i class="fas fa-arrow-right"></i>
                        </a>
                    </div>

                    <div class="sidebar-card">
                        <div class="sidebar-header"><i class="fas fa-star"></i> Popular Services</div>
                        {% if services %}
                            {% for service in services|slice:":4" %}
                            <a href="{% url 'client_search' %}?q={{ service.name|urlencode }}" class="sidebar-item">
                                <span><i class="fas fa-wrench"></i> {{ service.name }}</span>
                                <span>{{ service.providers.count }}</span>
                            </a>
                            {% endfor %}
                        {% endif %}
                    </div>
                </div>
            </div>

        <!-- ==================== PROVIDER DASHBOARD ==================== -->
        {% elif user.role == 'provider' %}

            <!-- Welcome Banner -->
            <div class="welcome-banner">
                <div class="stats-row">
                    <div class="stat-item">
                        <div class="value">{{ total_requests|default:0 }}</div>
                        <div class="label">Total</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">{{ accepted_requests|default:0 }}</div>
                        <div class="label">Active</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">{{ completed_requests|default:0 }}</div>
                        <div class="label">Completed</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">UGX {{ total_earnings|default:"0"|floatformat:0 }}</div>
                        <div class="label">Earnings</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">{{ user.average_rating|default:"0.0" }}</div>
                        <div class="label">Rating</div>
                    </div>
                </div>
            </div>

            <div class="dashboard-grid">
                <!-- Main Content -->
                <div>
                    <!-- Tabs -->
                    <div class="tabs">
                        <button class="tab-btn active" onclick="showTab('incoming')">
                            <i class="fas fa-inbox"></i> Incoming
                            {% if pending_requests > 0 %}
                                <span class="badge bg-danger" style="margin-left: 5px;">{{ pending_requests }}</span>
                            {% endif %}
                        </button>
                        <button class="tab-btn" onclick="showTab('active')">
                            <i class="fas fa-play-circle"></i> Active
                        </button>
                        <button class="tab-btn" onclick="showTab('completed')">
                            <i class="fas fa-check-circle"></i> Completed
                        </button>
                    </div>

                    <!-- Incoming Requests Tab -->
                    <div id="incoming-tab" class="tab-content active">
                        <div class="section-title"><i class="fas fa-clock"></i> WAITING FOR RESPONSE</div>
                        {% if requests %}
                            {% for req in requests %}
                                {% if req.status == 'pending' or req.status == 'negotiating' %}
                                <div class="list-item">
                                    <div class="item-info">
                                        <div class="item-title">{{ req.service_need.service_display|default:req.service.name }}</div>
                                        <div class="item-meta">
                                            <span><i class="fas fa-user"></i> {{ req.client.username }}</span>
                                            <span><i class="fas fa-calendar"></i> {{ req.created_at|date:"M d" }}</span>
                                            <span><i class="fas fa-money-bill"></i> UGX {{ req.amount|floatformat:0 }}</span>
                                        </div>
                                    </div>
                                    <div class="item-status">
                                        <span class="badge badge-{{ req.status }}">{{ req.status }}</span>
                                    </div>
                                    <div class="item-actions">
                                        <form method="post" action="{% url 'update_request_status' req.id 'accepted' %}" style="display: inline;">
                                            {% csrf_token %}
                                            <button type="submit" class="btn btn-success btn-sm" onclick="return confirm('Accept?')">Accept</button>
                                        </form>
                                        <form method="post" action="{% url 'update_request_status' req.id 'rejected' %}" style="display: inline;">
                                            {% csrf_token %}
                                            <button type="submit" class="btn btn-danger btn-sm" onclick="return confirm('Reject?')">Reject</button>
                                        </form>
                                    </div>
                                </div>
                                {% endif %}
                            {% endfor %}
                        {% else %}
                            <div class="empty-state">No incoming requests</div>
                        {% endif %}
                    </div>

                    <!-- Active Jobs Tab -->
                    <div id="active-tab" class="tab-content">
                        <div class="section-title"><i class="fas fa-play-circle"></i> ACTIVE JOBS</div>
                        {% if requests %}
                            {% for req in requests %}
                                {% if req.status == 'accepted' or req.status == 'paid' or req.status == 'in_progress' %}
                                <div class="list-item">
                                    <div class="item-info">
                                        <div class="item-title">{{ req.service_need.service_display|default:req.service.name }}</div>
                                        <div class="item-meta">
                                            <span><i class="fas fa-user"></i> {{ req.client.username }}</span>
                                            <span><i class="fas fa-calendar"></i> {{ req.created_at|date:"M d" }}</span>
                                        </div>
                                    </div>
                                    <div class="item-status">
                                        <span class="badge badge-{{ req.status }}">{{ req.status }}</span>
                                    </div>
                                    <div class="item-actions">
                                        {% if req.status == 'paid' %}
                                            <form method="post" action="{% url 'update_request_status' req.id 'in_progress' %}">
                                                {% csrf_token %}
                                                <button type="submit" class="btn btn-warning btn-sm">Start</button>
                                            </form>
                                        {% endif %}
                                        {% if req.status == 'in_progress' %}
                                            <a href="{% url 'provider_confirm_completion' req.id %}" class="btn btn-success btn-sm">Complete</a>
                                        {% endif %}
                                        <a href="{% url 'service_request_detail' req.id %}" class="btn btn-outline btn-sm">Details</a>
                                    </div>
                                </div>
                                {% endif %}
                            {% endfor %}
                        {% else %}
                            <div class="empty-state">No active jobs</div>
                        {% endif %}
                    </div>

                    <!-- Completed Jobs Tab -->
                    <div id="completed-tab" class="tab-content">
                        <div class="section-title"><i class="fas fa-check-circle"></i> RECENTLY COMPLETED</div>
                        {% if requests %}
                            {% for req in requests %}
                                {% if req.status == 'completed' %}
                                <div class="list-item">
                                    <div class="item-info">
                                        <div class="item-title">{{ req.service_need.service_display|default:req.service.name }}</div>
                                        <div class="item-meta">
                                            <span><i class="fas fa-user"></i> {{ req.client.username }}</span>
                                            <span><i class="fas fa-calendar"></i> {{ req.completed_at|date:"M d"|default:req.created_at|date:"M d" }}</span>
                                        </div>
                                    </div>
                                    <div class="item-status">
                                        <span class="badge badge-completed">completed</span>
                                    </div>
                                    <div class="item-actions">
                                        <a href="{% url 'service_request_detail' req.id %}" class="btn btn-outline btn-sm">View</a>
                                    </div>
                                </div>
                                {% endif %}
                            {% endfor %}
                        {% else %}
                            <div class="empty-state">No completed jobs yet</div>
                        {% endif %}
                    </div>
                </div>

                <!-- Sidebar -->
                <div class="sidebar">
                    <div class="sidebar-card">
                        <div class="sidebar-header"><i class="fas fa-chart-line"></i> Performance</div>
                        <div class="sidebar-item">
                            <span>Completion Rate</span>
                            <strong>{{ completion_rate|default:0 }}%</strong>
                        </div>
                        <div class="sidebar-item">
                            <span>Response Time</span>
                            <strong>{{ avg_response_time|default:0 }} min</strong>
                        </div>
                    </div>

                    <div class="sidebar-card">
                        <div class="sidebar-header"><i class="fas fa-bolt"></i> Quick Actions</div>
                        <a href="{% url 'upload_work_image' %}" class="sidebar-item">
                            <span><i class="fas fa-upload"></i> Upload Work</span>
                            <i class="fas fa-arrow-right"></i>
                        </a>
                        <a href="{% url 'provider_availability' %}" class="sidebar-item">
                            <span><i class="fas fa-calendar"></i> Set Availability</span>
                            <i class="fas fa-arrow-right"></i>
                        </a>
                        <a href="{% url 'request_withdrawal' %}" class="sidebar-item">
                            <span><i class="fas fa-money-bill"></i> Withdraw</span>
                            <i class="fas fa-arrow-right"></i>
                        </a>
                        <a href="{% url 'provider_profile' %}" class="sidebar-item">
                            <span><i class="fas fa-user-edit"></i> Edit Profile</span>
                            <i class="fas fa-arrow-right"></i>
                        </a>
                    </div>

                    <div class="sidebar-card">
                        <div class="sidebar-header"><i class="fas fa-star"></i> Your Rating</div>
                        <div class="sidebar-item" style="justify-content: center;">
                            <div style="text-align: center;">
                                <div style="font-size: 2rem; font-weight: 800;">{{ user.average_rating|default:"0.0" }}</div>
                                <div class="text-muted" style="font-size: 0.7rem;">from {{ user.total_ratings }} reviews</div>
                                <a href="{% url 'provider_ratings' user.id %}" style="font-size: 0.7rem;">View Reviews</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        <!-- ==================== ADMIN DASHBOARD ==================== -->
        {% elif user.role == 'admin' %}
            <div class="welcome-banner">
                <div class="stats-row">
                    <div class="stat-item">
                        <div class="value">{{ total_users|default:0 }}</div>
                        <div class="label">Users</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">{{ total_providers|default:0 }}</div>
                        <div class="label">Providers</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">{{ total_clients|default:0 }}</div>
                        <div class="label">Clients</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">UGX {{ total_revenue|default:0|floatformat:0 }}</div>
                        <div class="label">Revenue</div>
                    </div>
                </div>
            </div>
            <div class="dashboard-grid">
                <div>
                    <div class="list-item">
                        <a href="{% url 'admin_dashboard' %}" class="btn btn-primary">Full Admin Dashboard</a>
                        <a href="/admin/" class="btn btn-outline">Django Admin</a>
                    </div>
                </div>
                <div>
                    <div class="sidebar-card">
                        <div class="sidebar-header">Admin Actions</div>
                        <a href="{% url 'admin_withdrawals' %}" class="sidebar-item">Pending Withdrawals</a>
                        <a href="{% url 'admin_disputes' %}" class="sidebar-item">Disputes</a>
                    </div>
                </div>
            </div>
        {% else %}
            <div class="empty-state">No dashboard available</div>
        {% endif %}
    </main>

    <script>
        function showTab(tabId) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            // Show selected tab
            document.getElementById(tabId + '-tab').classList.add('active');
            
            // Update active button
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.textContent.toLowerCase().includes(tabId)) {
                    btn.classList.add('active');
                }
            });
        }

        function getCookie(name) {
            let value = null;
            if (document.cookie && document.cookie !== '') {
                document.cookie.split(';').forEach(cookie => {
                    let c = cookie.trim();
                    if (c.substring(0, name.length + 1) === (name + '=')) {
                        value = decodeURIComponent(c.substring(name.length + 1));
                    }
                });
            }
            return value;
        }
        
        function updateUserLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    fetch("{% url 'update_location' %}", {
                        method: "POST",
                        headers: { 
                            "Content-Type": "application/x-www-form-urlencoded", 
                            "X-CSRFToken": getCookie('csrftoken') 
                        },
                        body: `latitude=${position.coords.latitude}&longitude=${position.coords.longitude}`
                    }).then(() => location.reload());
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }
    </script>
</body>
</html>
