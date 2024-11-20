# Combined Python and HTML files
# Generated from directory: C:\Users\isultan\Documents\khcc_psut_ai_lab\khcc_psut_ai_lab
# Total files found: 65



# Contents from: .\templates\base.html
{% load static %}
{% load django_bootstrap5 %}
{% load crispy_forms_tags %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}KHCC AI Lab{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    {% bootstrap_css %}
    
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.css">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    {{ block.super }}
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'includes/navbar.html' %}
    
    <main class="py-4">
        {% bootstrap_messages %}
        
        {% block content %}
        {% endblock %}
    </main>
    
    <footer class="bg-light mt-5 py-4">
        <div class="container">
            <div class="text-center text-muted">
                <p>&copy; 2024 KHCC AI Lab. All rights reserved.</p>
            </div>
        </div>
    </footer>
    
    <!-- Bootstrap JavaScript -->
    {% bootstrap_javascript %}
    
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    
    <!-- Custom JavaScript -->
    <script src="{% static 'js/main.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>

# Contents from: .\templates\includes\navbar.html
<!-- templates/includes/navbar.html -->
<nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
    <div class="container">
        <a class="navbar-brand" href="{% url 'projects:project_list' %}">
            KHCC AI Lab
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                data-bs-target="#navbarNav" aria-controls="navbarNav" 
                aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a class="nav-link {% if request.resolver_match.url_name == 'project_list' and request.resolver_match.namespace == 'projects' %}active{% endif %}" 
                       href="{% url 'projects:project_list' %}">Seeds</a>
                </li>
                {% if user.is_authenticated %}
                <li class="nav-item">
                    <a class="nav-link {% if request.resolver_match.url_name == 'submit_project' and request.resolver_match.namespace == 'projects' %}active{% endif %}" 
                       href="{% url 'projects:submit_project' %}">Share</a>
                </li>
                {% endif %}
            </ul>
            <ul class="navbar-nav">
                {% if user.is_authenticated %}
                <li class="nav-item dropdown me-2">
                    <a class="nav-link position-relative" href="#" id="notificationsDropdown" 
                       role="button" data-bs-toggle="dropdown">
                        <i class="bi bi-bell"></i>
                        {% if unread_notifications_count %}
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                {{ unread_notifications_count }}
                            </span>
                        {% endif %}
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><h6 class="dropdown-header">Notifications</h6></li>
                        {% if notifications %}
                            {% for notification in notifications %}
                                <li>
                                    <a class="dropdown-item {% if not notification.is_read %}fw-bold{% endif %}" 
                                       href="{% url 'projects:mark_notification_read' notification.id %}">
                                        {{ notification.message }}
                                    </a>
                                </li>
                            {% endfor %}
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item text-center" href="{% url 'projects:notifications' %}">
                                    View All
                                </a>
                            </li>
                        {% else %}
                            <li><span class="dropdown-item-text">No new notifications</span></li>
                        {% endif %}
                    </ul>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button"
                       data-bs-toggle="dropdown" aria-expanded="false">
                        {{ user.username }}
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                        <li>
                            <a class="dropdown-item" href="{% url 'projects:user_profile' user.username %}">
                                <i class="bi bi-person"></i> Profile
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="{% url 'projects:edit_profile' %}">
                                <i class="bi bi-gear"></i> Settings
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item" href="{% url 'account_logout' %}">
                                <i class="bi bi-box-arrow-right"></i> Logout
                            </a>
                        </li>
                    </ul>
                </li>
                {% else %}
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'account_login' %}">Sign In</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'account_signup' %}">Sign Up</a>
                </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>

# Contents from: .\templates\includes\pagination.html
<!-- templates/projects/includes/pagination.html -->
{% if page_obj.has_other_pages %}
<nav aria-label="Project pagination" class="my-4">
    <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
        <li class="page-item">
            <a class="page-link" href="?page=1" aria-label="First">
                <span aria-hidden="true">&laquo;&laquo;</span>
            </a>
        </li>
        <li class="page-item">
            <a class="page-link" 
               href="?page={{ page_obj.previous_page_number }}" 
               aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
            </a>
        </li>
        {% endif %}

        {% for num in page_obj.paginator.page_range %}
            {% if page_obj.number == num %}
                <li class="page-item active">
                    <span class="page-link">{{ num }}</span>
                </li>
            {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ num }}">{{ num }}</a>
                </li>
            {% endif %}
        {% endfor %}

        {% if page_obj.has_next %}
        <li class="page-item">
            <a class="page-link" 
               href="?page={{ page_obj.next_page_number }}" 
               aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
            </a>
        </li>
        <li class="page-item">
            <a class="page-link" 
               href="?page={{ page_obj.paginator.num_pages }}" 
               aria-label="Last">
                <span aria-hidden="true">&raquo;&raquo;</span>
            </a>
        </li>
        {% endif %}
    </ul>
</nav>
{% endif %}

# Contents from: .\templates\navbar.html
<nav class="navbar navbar-expand-lg navbar-light bg-light"></nav>
    <div class="container">
        <!-- Brand -->
        <a class="navbar-brand" href="{% url 'projects:project_list' %}">
            <i class="bi bi-code-square"></i> AI Lab Seeds
        </a>

        <!-- Toggle Button -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
            <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Navbar Content -->
        <div class="collapse navbar-collapse" id="navbarContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <!-- Seeds -->
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="projectsDropdown" role="button" data-bs-toggle="dropdown">
                        <i class="bi bi-folder"></i> Seeds
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="{% url 'projects:project_list' %}">Browse All</a></li>
                        <li><a class="dropdown-item" href="{% url 'projects:search_projects' %}">Search Seeds</a></li>
                        <li><a class="dropdown-item" href="{% url 'projects:leaderboard' %}">Leaderboard</a></li>
                        {% if user.is_authenticated %}
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{% url 'projects:submit_project' %}">Submit Seed</a></li>
                        {% endif %}
                    </ul>
                </li>

                <!-- Community -->
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'projects:leaderboard' %}">
                        <i class="bi bi-trophy"></i> Leaderboard
                    </a>
                </li>
            </ul>

            <!-- Search Form -->
            <form class="d-flex me-3" action="{% url 'projects:search_projects' %}" method="GET">
                <div class="input-group">
                    <input class="form-control" type="search" name="query" placeholder="Search seeds...">
                    <button class="btn btn-outline-primary" type="submit">
                        <i class="bi bi-search"></i>
                    </button>
                </div>
            </form>

            <!-- User Menu -->
            {% if user.is_authenticated %}
                <ul class="navbar-nav">
                    <!-- Notifications -->
                    <li class="nav-item dropdown me-2">
                        <a class="nav-link position-relative" href="#" id="notificationsDropdown" 
                           role="button" data-bs-toggle="dropdown">
                            <i class="bi bi-bell"></i>
                            {% if unread_notifications_count %}
                                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                    {{ unread_notifications_count }}
                                </span>
                            {% endif %}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li><h6 class="dropdown-header">Notifications</h6></li>
                            {% if notifications %}
                                {% for notification in notifications|slice:":5" %}
                                    <li><a class="dropdown-item" href="#">{{ notification.message }}</a></li>
                                {% endfor %}
                                <li><hr class="dropdown-divider"></li>
                                <li>
                                    <a class="dropdown-item text-center" href="{% url 'projects:notifications' %}">
                                        View All
                                    </a>
                                </li>
                            {% else %}
                                <li><span class="dropdown-item-text">No new notifications</span></li>
                            {% endif %}
                        </ul>
                    </li>

                    <!-- User Profile -->
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                            {% if user.profile.avatar %}
                                <img src="{{ user.profile.avatar.url }}" alt="{{ user.username }}" 
                                     class="rounded-circle" style="width: 24px; height: 24px;">
                            {% else %}
                                <i class="bi bi-person-circle"></i>
                            {% endif %}
                            {{ user.username }}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li>
                                <a class="dropdown-item" href="{% url 'projects:user_profile' user.username %}">
                                    <i class="bi bi-person"></i> My Profile
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="{% url 'projects:user_projects' user.username %}">
                                    <i class="bi bi-folder"></i> My Seeds
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="{% url 'projects:notifications' %}">
                                    <i class="bi bi-bell"></i> Notifications
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="{% url 'projects:edit_profile' %}">
                                    <i class="bi bi-gear"></i> Settings
                                </a>
                            </li>
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item text-danger" href="{% url 'account_logout' %}">
                                    <i class="bi bi-box-arrow-right"></i> Logout
                                </a>
                            </li>
                        </ul>
                    </li>
                </ul>
            {% else %}
                <div class="navbar-nav">
                    <a class="nav-link" href="{% url 'account_login' %}">Sign In</a>
                    <a class="nav-link" href="{% url 'account_signup' %}">Sign Up</a>
                </div>
            {% endif %}
        </div>
    </div>
</nav>

# Contents from: .\templates\projects\about.html
{% extends 'base.html' %}
{% load static %}

{% block title %}About - KHCC AI Lab{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="hero bg-primary text-white py-5 mb-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-8 mx-auto text-center">
                <h1 class="display-4 fw-bold mb-4">About KHCC AI Lab</h1>
                <p class="lead mb-0">
                    A collaborative initiative between King Hussein Cancer Center and 
                    Princess Sumaya University for Technology to advance AI in healthcare.
                </p>
            </div>
        </div>
    </div>
</section>

<!-- Mission Section -->
<section class="mission mb-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Our Mission</h2>
                <p class="lead mb-5">
                    To foster innovation and collaboration in artificial intelligence 
                    applications for healthcare, particularly in cancer research and treatment.
                </p>
            </div>
        </div>
        
        <div class="row g-4">
            <div class="col-md-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body text-center">
                        <i class="bi bi-lightbulb display-4 text-primary mb-3"></i>
                        <h3 class="h5 mb-3">Innovation</h3>
                        <p class="text-muted mb-0">
                            Developing cutting-edge AI solutions to improve cancer diagnosis, 
                            treatment, and patient care.
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body text-center">
                        <i class="bi bi-people display-4 text-primary mb-3"></i>
                        <h3 class="h5 mb-3">Collaboration</h3>
                        <p class="text-muted mb-0">
                            Bringing together medical professionals, researchers, and 
                            technology experts to solve complex healthcare challenges.
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body text-center">
                        <i class="bi bi-mortarboard display-4 text-primary mb-3"></i>
                        <h3 class="h5 mb-3">Education</h3>
                        <p class="text-muted mb-0">
                            Training the next generation of AI specialists in healthcare 
                            through hands-on projects and research opportunities.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Partners Section -->
<section class="partners bg-light py-5 mb-5">
    <div class="container">
        <h2 class="h3 text-center mb-5">Our Partner Institutions</h2>
        
        <div class="row justify-content-center">
            <div class="col-lg-6 mb-4 mb-lg-0">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body">
                        <div class="text-center mb-4">
                            <img src="{% static 'images/khcc-logo.png' %}" 
                                 alt="King Hussein Cancer Center" 
                                 class="img-fluid" 
                                 style="max-height: 100px;">
                        </div>
                        <h3 class="h5 text-center mb-3">King Hussein Cancer Center</h3>
                        <p class="text-muted">
                            A leading comprehensive cancer care center in the Middle East, 
                            providing state-of-the-art medical services and conducting 
                            groundbreaking research in cancer treatment.
                        </p>
                        <div class="text-center">
                            <a href="https://khcc.jo" 
                               target="_blank" 
                               class="btn btn-outline-primary">
                                Visit Website
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-lg-6">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body">
                        <div class="text-center mb-4">
                            <img src="{% static 'images/psut-logo.png' %}" 
                            alt="Princess Sumaya University for Technology" 
                            class="img-fluid" 
                            style="max-height: 100px;">
                   </div>
                   <h3 class="h5 text-center mb-3">Princess Sumaya University for Technology</h3>
                   <p class="text-muted">
                       A leading technical university in Jordan, specializing in IT, 
                       engineering, and artificial intelligence education and research.
                   </p>
                   <div class="text-center">
                       <a href="https://www.psut.edu.jo" 
                          target="_blank" 
                          class="btn btn-outline-primary">
                           Visit Website
                       </a>
                   </div>
               </div>
           </div>
       </div>
   </div>
</div>
</section>

<!-- Research Areas Section -->
<section class="research-areas mb-5">
<div class="container">
   <h2 class="h3 text-center mb-5">Our Research Areas</h2>
   
   <div class="row g-4">
       <div class="col-md-6 col-lg-4">
           <div class="card border-0 shadow-sm h-100">
               <div class="card-body">
                   <div class="d-flex align-items-center mb-3">
                       <i class="bi bi-camera text-primary fs-4 me-2"></i>
                       <h4 class="h5 mb-0">Medical Imaging AI</h4>
                   </div>
                   <p class="text-muted mb-0">
                       Developing advanced algorithms for cancer detection and diagnosis 
                       using medical imaging.
                   </p>
               </div>
           </div>
       </div>
       
       <div class="col-md-6 col-lg-4">
           <div class="card border-0 shadow-sm h-100">
               <div class="card-body">
                   <div class="d-flex align-items-center mb-3">
                       <i class="bi bi-graph-up text-primary fs-4 me-2"></i>
                       <h4 class="h5 mb-0">Predictive Analytics</h4>
                   </div>
                   <p class="text-muted mb-0">
                       Using machine learning for treatment outcome prediction and 
                       personalized medicine.
                   </p>
               </div>
           </div>
       </div>
       
       <div class="col-md-6 col-lg-4">
           <div class="card border-0 shadow-sm h-100">
               <div class="card-body">
                   <div class="d-flex align-items-center mb-3">
                       <i class="bi bi-clipboard-data text-primary fs-4 me-2"></i>
                       <h4 class="h5 mb-0">Clinical Data Analysis</h4>
                   </div>
                   <p class="text-muted mb-0">
                       Mining and analyzing clinical data to identify patterns and 
                       improve patient care.
                   </p>
               </div>
           </div>
       </div>
       
       <div class="col-md-6 col-lg-4">
           <div class="card border-0 shadow-sm h-100">
               <div class="card-body">
                   <div class="d-flex align-items-center mb-3">
                       <i class="bi bi-robot text-primary fs-4 me-2"></i>
                       <h4 class="h5 mb-0">Natural Language Processing</h4>
                   </div>
                   <p class="text-muted mb-0">
                       Processing medical records and research papers to extract 
                       valuable insights.
                   </p>
               </div>
           </div>
       </div>
       
       <div class="col-md-6 col-lg-4">
           <div class="card border-0 shadow-sm h-100">
               <div class="card-body">
                   <div class="d-flex align-items-center mb-3">
                       <i class="bi bi-heart-pulse text-primary fs-4 me-2"></i>
                       <h4 class="h5 mb-0">Patient Monitoring</h4>
                   </div>
                   <p class="text-muted mb-0">
                       Real-time monitoring systems using AI for improved patient care 
                       and early intervention.
                   </p>
               </div>
           </div>
       </div>
       
       <div class="col-md-6 col-lg-4">
           <div class="card border-0 shadow-sm h-100">
               <div class="card-body">
                   <div class="d-flex align-items-center mb-3">
                       <i class="bi bi-shield-check text-primary fs-4 me-2"></i>
                       <h4 class="h5 mb-0">Drug Discovery</h4>
                   </div>
                   <p class="text-muted mb-0">
                       Accelerating drug discovery and development using artificial 
                       intelligence algorithms.
                   </p>
               </div>
           </div>
       </div>
   </div>
</div>
</section>

<!-- Team Section -->
<section class="team bg-light py-5 mb-5">
<div class="container">
   <h2 class="h3 text-center mb-5">Leadership Team</h2>
   
   <div class="row g-4">
       <div class="col-md-6 col-lg-3">
           <div class="card border-0 shadow-sm text-center h-100">
               <div class="card-body">
                   <img src="{% static 'images/team/director.jpg' %}" 
                        alt="Lab Director" 
                        class="rounded-circle mb-3" 
                        style="width: 150px; height: 150px; object-fit: cover;">
                   <h4 class="h5 mb-1">Dr. John Doe</h4>
                   <p class="text-muted small mb-3">Lab Director</p>
                   <p class="text-muted small mb-3">
                       20+ years experience in medical AI research and implementation.
                   </p>
                   <div class="d-flex justify-content-center gap-2">
                       <a href="#" class="text-dark"><i class="bi bi-linkedin"></i></a>
                       <a href="#" class="text-dark"><i class="bi bi-twitter"></i></a>
                       <a href="#" class="text-dark"><i class="bi bi-envelope"></i></a>
                   </div>
               </div>
           </div>
       </div>
       
       <!-- Add more team members here -->
   </div>
</div>
</section>

<!-- Join Us Section -->
<section class="join-us mb-5">
<div class="container">
   <div class="card border-0 bg-primary text-white shadow">
       <div class="card-body text-center py-5">
           <h2 class="h3 mb-4">Join Our Research Team</h2>
           <p class="lead mb-4">
               We're always looking for talented researchers and students to join our team. 
               If you're passionate about AI in healthcare, we'd love to hear from you.
           </p>
           <a href="{% url 'contact' %}" class="btn btn-light btn-lg">
               Contact Us
           </a>
       </div>
   </div>
</div>
</section>
{% endblock %}

# Contents from: .\templates\projects\edit_profile.html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card border-0 shadow-sm">
                <div class="card-body">
                    <h4 class="card-title mb-4">Edit Profile</h4>
                    
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <div class="mb-4">
                            <div class="d-flex justify-content-center">
                                {% if profile.avatar %}
                                    <img src="{{ profile.avatar.url }}" 
                                         alt="Current avatar" 
                                         class="rounded-circle mb-3" 
                                         style="width: 150px; height: 150px; object-fit: cover;">
                                {% else %}
                                    <img src="https://ui-avatars.com/api/?name={{ user.username }}&size=150" 
                                         alt="Default avatar" 
                                         class="rounded-circle mb-3">
                                {% endif %}
                            </div>
                            <div class="mb-3">
                                {{ form.avatar|as_crispy_field }}
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-12 mb-3">
                                {{ form.bio|as_crispy_field }}
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                {{ form.location|as_crispy_field }}
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                {{ form.github_username|as_crispy_field }}
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                {{ form.website|as_crispy_field }}
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                {{ form.linkedin_url|as_crispy_field }}
                            </div>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">
                                Save Changes
                            </button>
                            <a href="{% url 'user_profile' username=user.username %}" 
                               class="btn btn-outline-secondary">
                                Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\templates\projects\edit_project.html
<!-- templates/projects/edit_project.html -->
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% load static %}

{% block title %}Edit {{ project.title }} - KHCC AI Lab{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h2 class="card-title mb-4">Edit Project</h2>
                    
                    <form method="post" enctype="multipart/form-data" id="editProjectForm">
                        {% csrf_token %}
                        
                        <!-- Current Featured Image Preview -->
                        {% if project.featured_image %}
                        <div class="mb-4">
                            <label class="form-label">Current Featured Image</label>
                            <div class="position-relative">
                                <img src="{{ project.featured_image.url }}" 
                                     alt="Current featured image" 
                                     class="img-fluid rounded">
                                <button type="button" 
                                        class="btn btn-sm btn-danger position-absolute top-0 end-0 m-2"
                                        id="removeFeaturedImage">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </div>
                        </div>
                        {% endif %}
                        
                        <!-- Form Fields -->
                        {{ form|crispy }}
                        
                        <!-- Current Files -->
                        <div class="card bg-light mb-4">
                            <div class="card-body">
                                <h5 class="card-title">Current Files</h5>
                                
                                {% if project.pdf_file %}
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <div>
                                        <i class="bi bi-file-pdf text-danger me-2"></i>
                                        Documentation.pdf
                                        <span class="text-muted ms-2">
                                            ({{ project.pdf_file.size|filesizeformat }})
                                        </span>
                                    </div>
                                    <button type="button" 
                                            class="btn btn-sm btn-danger" 
                                            id="removePdfFile">
                                        Remove
                                    </button>
                                </div>
                                {% endif %}
                                
                                {% if project.additional_files %}
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <i class="bi bi-file-earmark me-2"></i>
                                        {{ project.additional_files.name|split:'/'|last }}
                                        <span class="text-muted ms-2">
                                            ({{ project.additional_files.size|filesizeformat }})
                                        </span>
                                    </div>
                                    <button type="button" 
                                            class="btn btn-sm btn-danger" 
                                            id="removeAdditionalFiles">
                                        Remove
                                    </button>
                                </div>
                                {% endif %}
                                
                                {% if not project.pdf_file and not project.additional_files %}
                                <p class="text-muted mb-0">No files currently uploaded</p>
                                {% endif %}
                            </div>
                        </div>
                        
                        <!-- Preview Section -->
                        <div class="card mb-4">
                            <div class="card-header">
                                <h5 class="card-title mb-0">Preview</h5>
                            </div>
                            <div class="card-body">
                                <h3 id="previewTitle"></h3>
                                <p id="previewDescription" class="text-muted"></p>
                                <div id="previewTags"></div>
                            </div>
                        </div>
                        
                        <div class="d-flex justify-content-between">
                            <button type="button" 
                                    class="btn btn-light" 
                                    onclick="history.back()">
                                Cancel
                            </button>
                            <div class="d-flex gap-2">
                                <button type="button" 
                                        class="btn btn-danger" 
                                        data-bs-toggle="modal" 
                                        data-bs-target="#deleteProjectModal">
                                    Delete Project
                                </button>
                                <button type="submit" class="btn btn-primary">
                                    Save Changes
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Delete Project Modal -->
<div class="modal fade" id="deleteProjectModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Delete Project</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="alert alert-danger">
                    <h6 class="alert-heading">Warning!</h6>
                    <p class="mb-0">This action cannot be undone. All project data, including:</p>
                    <ul class="mb-0">
                        <li>Comments and ratings</li>
                        <li>Uploaded files</li>
                        <li>Analytics data</li>
                        <li>Associated notifications</li>
                    </ul>
                    <p class="mb-0">will be permanently deleted.</p>
                </div>
                <p>Please type <strong>{{ project.title }}</strong> to confirm deletion:</p>
                <input type="text" 
                       class="form-control" 
                       id="confirmProjectTitle" 
                       placeholder="Type project title">
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-light" data-bs-dismiss="modal">
                    Cancel
                </button>
                <form method="post" action="{% url 'projects:delete_project' project.pk %}">
                    {% csrf_token %}
                    <button type="submit" 
                            class="btn btn-danger" 
                            id="confirmDeleteBtn" 
                            disabled>
                        Delete Project
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
$(document).ready(function() {
    // Live preview functionality
    function updatePreview() {
        $('#previewTitle').text($('#id_title').val());
        $('#previewDescription').text($('#id_description').val());
        
        const tags = $('#id_tags').val().split(',').map(tag => tag.trim()).filter(Boolean);
        $('#previewTags').html(
            tags.map(tag => 
                `<span class="badge bg-light text-dark me-1">${tag}</span>`
            ).join('')
        );
    }
    
    $('#id_title, #id_description, #id_tags').on('input', updatePreview);
    updatePreview();  // Initial preview
    
    // Handle file removals
    $('#removeFeaturedImage').click(function() {
        if (confirm('Remove featured image?')) {
            // Add hidden input to indicate image removal
            $('<input>').attr({
                type: 'hidden',
                name: 'remove_featured_image',
                value: 'true'
            }).appendTo('#editProjectForm');
            
            $(this).closest('.mb-4').remove();
        }
    });
    
    $('#removePdfFile').click(function() {
        if (confirm('Remove PDF file?')) {
            $('<input>').attr({
                type: 'hidden',
                name: 'remove_pdf',
                value: 'true'
            }).appendTo('#editProjectForm');
            
            $(this).closest('.d-flex').remove();
        }
    });
    
    $('#removeAdditionalFiles').click(function() {
        if (confirm('Remove additional files?')) {
            $('<input>').attr({
                type: 'hidden',
                name: 'remove_additional_files',
                value: 'true'
            }).appendTo('#editProjectForm');
            
            $(this).closest('.d-flex').remove();
        }
    });
    
    // Handle delete confirmation
    $('#confirmProjectTitle').on('input', function() {
        const deleteBtn = $('#confirmDeleteBtn');
        if ($(this).val() === '{{ project.title }}') {
            deleteBtn.prop('disabled', false);
        } else {
            deleteBtn.prop('disabled', true);
        }
    });
    
    // File upload preview
    function handleFileSelect(event, previewId) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $(`#${previewId}`).attr('src', e.target.result);
            };
            reader.readAsDataURL(file);
        }
    }
    
    $('#id_featured_image').change(function(e) {
        handleFileSelect(e, 'featuredImagePreview');
    });
});
</script>
{% endblock %}

# Contents from: .\templates\projects\email.html
<!-- templates/emails/base_email.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ subject }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #007bff;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 20px;
            background-color: #ffffff;
        }
        .footer {
            text-align: center;
            padding: 20px;
            background-color: #f8f9fa;
            color: #666;
            font-size: 12px;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px 0;
        }
        .social-links {
            margin-top: 20px;
        }
        .social-links a {
            color: #666;
            text-decoration: none;
            margin: 0 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>KHCC AI Lab</h1>
        </div>
        <div class="content">
            {% block content %}{% endblock %}
        </div>
        <div class="footer">
            <p>
                You received this email because you're part of the KHCC AI Lab community.
                If you don't want to receive these emails, you can 
                <a href="{{ unsubscribe_url }}">unsubscribe</a>.
            </p>
            <div class="social-links">
                <a href="#">LinkedIn</a> |
                <a href="#">Twitter</a> |
                <a href="#">GitHub</a>
            </div>
            <p>&copy; {% now "Y" %} KHCC AI Lab. All rights reserved.</p>
        </div>
    </div>
</body>
</html>

<!-- templates/emails/notification.html -->
{% extends 'emails/base_email.html' %}

{% block content %}
<h2>New Notification</h2>
<p>Hello {{ notification.recipient.get_full_name|default:notification.recipient.username }},</p>

<p>{{ notification.message }}</p>

{% if notification.project %}
<p>
    <a href="{{ site_url }}{% url 'project_detail' notification.project.pk %}" class="btn">
        View Project
    </a>
</p>
{% endif %}

<p>Best regards,<br>KHCC AI Lab Team</p>
{% endblock %}

<!-- templates/emails/welcome.html -->
{% extends 'emails/base_email.html' %}

{% block content %}
<h2>Welcome to KHCC AI Lab!</h2>
<p>Hello {{ user.get_full_name|default:user.username }},</p>

<p>
    Welcome to the KHCC AI Lab community! We're excited to have you join us in our 
    mission to advance AI applications in healthcare.
</p>

<h3>Getting Started</h3>
<ul>
    <li>Complete your profile</li>
    <li>Explore ongoing projects</li>
    <li>Connect with other researchers</li>
    <li>Share your own projects</li>
</ul>

<p>
    <a href="{{ site_url }}{% url 'edit_profile' %}" class="btn">
        Complete Your Profile
    </a>
</p>

<p>Best regards,<br>KHCC AI Lab Team</p>
{% endblock %}

<!-- templates/emails/project_comment.html -->
{% extends 'emails/base_email.html' %}

{% block content %}
<h2>New Comment on Your Seed</h2>
<p>Hello {{ project.author.get_full_name|default:project.author.username }},</p>

<p>{{ comment.user.get_full_name|default:comment.user.username }} commented on your project "{{ project.title }}":</p>

<blockquote style="border-left: 3px solid #007bff; padding-left: 10px; margin: 10px 0;">
    {{ comment.content }}
</blockquote>

<p>
    <a href="{{ site_url }}{% url 'project_detail' project.pk %}" class="btn">
        View Comment
    </a>
</p>

<p>Best regards,<br>KHCC AI Lab Team</p>
{% endblock %}

<!-- templates/emails/project_clap.html -->
{% extends 'emails/base_email.html' %}

{% block content %}
<h2>Someone Appreciated Your Seed</h2>
<p>Hello {{ project.author.get_full_name|default:project.author.username }},</p>

<p>{{ clap.user.get_full_name|default:clap.user.username }} clapped for your project "{{ project.title }}"!</p>

<p>Your project now has {{ project.claps }} claps in total.</p>

<p>
    <a href="{{ site_url }}{% url 'project_detail' project.pk %}" class="btn">
        View Project
    </a>
</p>

<p>Best regards,<br>KHCC AI Lab Team</p>
{% endblock %}

<!-- templates/emails/password_reset.html -->
{% extends 'emails/base_email.html' %}

{% block content %}
<h2>Password Reset Request</h2>
<p>Hello {{ user.get_full_name|default:user.username }},</p>

<p>
    We received a request to reset your password. If you didn't make this request, 
    you can safely ignore this email.
</p>

<p>
    To reset your password, click the button below:
</p>

<p>
    <a href="{{ password_reset_url }}" class="btn">
        Reset Password
    </a>
</p>

<p>
    If the button doesn't work, copy and paste this link into your browser:
    <br>
    {{ password_reset_url }}
</p>

<p>
    This link will expire in 24 hours for security reasons.
</p>

<p>Best regards,<br>KHCC AI Lab Team</p>
{% endblock %}

<!-- templates/emails/email_verification.html -->
{% extends 'emails/base_email.html' %}

{% block content %}
<h2>Verify Your Email Address</h2>
<p>Hello {{ user.get_full_name|default:user.username }},</p>

<p>
    Thank you for registering with KHCC AI Lab. Please verify your email address 
    by clicking the button below:
</p>

<p>
    <a href="{{ verification_url }}" class="btn">
        Verify Email Address
    </a>
</p>

<p>
    If the button doesn't work, copy and paste this link into your browser:
    <br>
    {{ verification_url }}
</p>

<p>
    This link will expire in 24 hours for security reasons.
</p>

<p>Best regards,<br>KHCC AI Lab Team</p>
{% endblock %}

# Contents from: .\templates\projects\faculty_page.html
{% extends 'base.html' %}
{% load static %}

{% block title %}Faculty - KHCC AI Lab{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="hero bg-primary text-white py-5 mb-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-8 mx-auto text-center">
                <h1 class="display-4 fw-bold mb-4">Our Faculty</h1>
                <p class="lead mb-0">
                    Meet our distinguished team of researchers, clinicians, and educators 
                    leading the advancement of AI in healthcare.
                </p>
            </div>
        </div>
    </div>
</section>

<!-- Leadership Section -->
<section class="leadership mb-5">
    <div class="container">
        <h2 class="h3 text-center mb-5">Leadership Team</h2>
        
        <div class="row g-4">
            <!-- Lab Director -->
            <div class="col-md-6 col-lg-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body text-center">
                        <img src="{% static 'images/faculty/director.jpg' %}" 
                             alt="Lab Director" 
                             class="rounded-circle mb-4" 
                             style="width: 200px; height: 200px; object-fit: cover;">
                        <h3 class="h4 mb-2">Prof. Ahmad Abdullah</h3>
                        <p class="text-primary mb-3">Lab Director</p>
                        <p class="text-muted mb-4">
                            Ph.D. in Artificial Intelligence<br>
                            20+ years experience in medical AI
                        </p>
                        <div class="d-flex justify-content-center gap-3 mb-4">
                            <a href="#" class="text-dark fs-5">
                                <i class="bi bi-linkedin"></i>
                            </a>
                            <a href="#" class="text-dark fs-5">
                                <i class="bi bi-google"></i>
                            </a>
                            <a href="#" class="text-dark fs-5">
                                <i class="bi bi-envelope"></i>
                            </a>
                        </div>
                        <button class="btn btn-outline-primary" 
                                data-bs-toggle="modal" 
                                data-bs-target="#directorModal">
                            View Profile
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Deputy Director -->
            <div class="col-md-6 col-lg-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body text-center">
                        <img src="{% static 'images/faculty/deputy.jpg' %}" 
                             alt="Deputy Director" 
                             class="rounded-circle mb-4" 
                             style="width: 200px; height: 200px; object-fit: cover;">
                        <h3 class="h4 mb-2">Dr. Sarah Smith</h3>
                        <p class="text-primary mb-3">Deputy Director</p>
                        <p class="text-muted mb-4">
                            Ph.D. in Medical Informatics<br>
                            Lead Researcher, Cancer Imaging AI
                        </p>
                        <div class="d-flex justify-content-center gap-3 mb-4">
                            <a href="#" class="text-dark fs-5">
                                <i class="bi bi-linkedin"></i>
                            </a>
                            <a href="#" class="text-dark fs-5">
                                <i class="bi bi-google"></i>
                            </a>
                            <a href="#" class="text-dark fs-5">
                                <i class="bi bi-envelope"></i>
                            </a>
                        </div>
                        <button class="btn btn-outline-primary" 
                                data-bs-toggle="modal" 
                                data-bs-target="#deputyModal">
                            View Profile
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Research Director -->
            <div class="col-md-6 col-lg-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body text-center">
                        <img src="{% static 'images/faculty/research.jpg' %}" 
                             alt="Research Director" 
                             class="rounded-circle mb-4" 
                             style="width: 200px; height: 200px; object-fit: cover;">
                        <h3 class="h4 mb-2">Dr. Mohammed Hassan</h3>
                        <p class="text-primary mb-3">Research Director</p>
                        <p class="text-muted mb-4">
                            Ph.D. in Computer Science<br>
                            Expert in Machine Learning for Healthcare
                        </p>
                        <div class="d-flex justify-content-center gap-3 mb-4">
                            <a href="#" class="text-dark fs-5">
                                <i class="bi bi-linkedin"></i>
                            </a>
                            <a href="#" class="text-dark fs-5">
                                <i class="bi bi-google"></i>
                            </a>
                            <a href="#" class="text-dark fs-5">
                                <i class="bi bi-envelope"></i>
                            </a>
                        </div>
                        <button class="btn btn-outline-primary" 
                                data-bs-toggle="modal" 
                                data-bs-target="#researchModal">
                            View Profile
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Research Faculty Section -->
<section class="research-faculty bg-light py-5 mb-5">
    <div class="container">
        <h2 class="h3 text-center mb-5">Research Faculty</h2>
        
        <div class="row g-4">
            <!-- Faculty Members -->
            {% for faculty in research_faculty %}
            <div class="col-md-6 col-lg-3">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body text-center">
                        <img src="{{ faculty.image.url }}" 
                             alt="{{ faculty.name }}" 
                             class="rounded-circle mb-3" 
                             style="width: 150px; height: 150px; object-fit: cover;">
                        <h3 class="h5 mb-2">{{ faculty.name }}</h3>
                        <p class="text-primary small mb-2">{{ faculty.title }}</p>
                        <p class="text-muted small mb-3">{{ faculty.specialization }}</p>
                        <div class="d-flex justify-content-center gap-2">
                            {% if faculty.linkedin_url %}
                            <a href="{{ faculty.linkedin_url }}" class="text-dark">
                                <i class="bi bi-linkedin"></i>
                            </a>
                            {% endif %}
                            {% if faculty.google_scholar %}
                            <a href="{{ faculty.google_scholar }}" class="text-dark">
                                <i class="bi bi-google"></i>
                            </a>
                            {% endif %}
                            {% if faculty.email %}
                            <a href="mailto:{{ faculty.email }}" class="text-dark">
                                <i class="bi bi-envelope"></i>
                            </a>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Clinical Faculty Section -->
<section class="clinical-faculty mb-5">
    <div class="container">
        <h2 class="h3 text-center mb-5">Clinical Faculty</h2>
        
        <div class="row g-4">
            <!-- Clinical Faculty Members -->
            {% for faculty in clinical_faculty %}
            <div class="col-md-6 col-lg-3">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body text-center">
                        <img src="{{ faculty.image.url }}" 
                             alt="{{ faculty.name }}" 
                             class="rounded-circle mb-3" 
                             style="width: 150px; height: 150px; object-fit: cover;">
                        <h3 class="h5 mb-2">{{ faculty.name }}</h3>
                        <p class="text-primary small mb-2">{{ faculty.title }}</p>
                        <p class="text-muted small mb-3">{{ faculty.department }}</p>
                        <div class="d-flex justify-content-center gap-2">
                            {% if faculty.linkedin_url %}
                            <a href="{{ faculty.linkedin_url }}" class="text-dark">
                                <i class="bi bi-linkedin"></i>
                            </a>
                            {% endif %}
                            {% if faculty.website %}
                            <a href="{{ faculty.website }}" class="text-dark">
                                <i class="bi bi-globe"></i>
                            </a>
                            {% endif %}
                            {% if faculty.email %}
                            <a href="mailto:{{ faculty.email }}" class="text-dark">
                                <i class="bi bi-envelope"></i>
                            </a>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Faculty Modals -->
{% for faculty in all_faculty %}
<div class="modal fade" id="modal{{ faculty.id }}" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header border-0">
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body text-center px-4 pb-5">
                <img src="{{ faculty.image.url }}" 
                     alt="{{ faculty.name }}" 
                     class="rounded-circle mb-4" 
                     style="width: 200px; height: 200px; object-fit: cover;">
                <h2 class="h4 mb-2">{{ faculty.name }}</h2>
                <p class="text-primary mb-4">{{ faculty.title }}</p>
                
                <div class="row mb-4">
                    <div class="col-md-6 mb-3 mb-md-0">
                        <h3 class="h6 text-uppercase mb-3">Education</h3>
                        <ul class="list-unstyled text-muted">
                            {% for education in faculty.education.all %}
                            <li class="mb-2">{{ education.degree }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h3 class="h6 text-uppercase mb-3">Research Interests</h3>
                        <ul class="list-unstyled text-muted">
                            {% for interest in faculty.research_interests.all %}
                            <li class="mb-2">{{ interest.name }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
                
                <div class="mb-4">
                    <h3 class="h6 text-uppercase mb-3">Biography</h3>
                    <p class="text-muted">{{ faculty.bio }}</p>
                </div>
                
                <div class="mb-4">
                    <h3 class="h6 text-uppercase mb-3">Selected Publications</h3>
                    <ul class="list-unstyled text-muted">
                        {% for publication in faculty.selected_publications.all %}
                        <li class="mb-2">{{ publication.citation }}</li>
                        {% endfor %}
                    </ul>
                </div>
                
                <div class="d-flex justify-content-center gap-3">
                    {% if faculty.linkedin_url %}
                    <a href="{{ faculty.linkedin_url }}" class="btn btn-outline-primary">
                        <i class="bi bi-linkedin"></i> LinkedIn
                    </a>
                    {% endif %}
                    {% if faculty.google_scholar %}
                    <a href="{{ faculty.google_scholar }}" class="btn btn-outline-primary">
                        <i class="bi bi-google"></i> Google Scholar
                    </a>
                    {% endif %}
                    {% if faculty.email %}
                    <a href="mailto:{{ faculty.email }}" class="btn btn-outline-primary">
                        <i class="bi bi-envelope"></i> Email
                    </a>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endfor %}

<!-- Join Us Section -->
<section class="join-us bg-light py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Join Our Faculty</h2>
                <p class="mb-4">
                    We're always looking for talented researchers and clinicians to join our team. 
                    If you're passionate about advancing AI in healthcare, we'd love to hear from you.
                </p>
                <a href="{% url 'careers' %}" class="btn btn-primary">
                    View Open Positions
                </a>
            </div>
        </div>
    </div>
</section>
{% endblock %}

# Contents from: .\templates\projects\faq.html
{% extends 'base.html' %}
{% load static %}

{% block title %}FAQ - KHCC AI Lab{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="hero bg-primary text-white py-5 mb-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-8 mx-auto text-center">
                <h1 class="display-4 fw-bold mb-4">Frequently Asked Questions</h1>
                <p class="lead mb-0">
                    Find answers to common questions about our AI Lab and collaboration opportunities.
                </p>
            </div>
        </div>
    </div>
</section>

<!-- FAQ Section -->
<section class="faq mb-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="accordion" id="faqAccordion">
                    <!-- General Questions -->
                    <div class="mb-4">
                        <h2 class="h4 mb-3">General Questions</h2>
                        
                        <div class="accordion-item border-0 shadow-sm mb-3">
                            <h3 class="accordion-header">
                                <button class="accordion-button" type="button" 
                                        data-bs-toggle="collapse" 
                                        data-bs-target="#faq1">
                                    What is KHCC AI Lab?
                                </button>
                            </h3>
                            <div id="faq1" class="accordion-collapse collapse show" 
                                 data-bs-parent="#faqAccordion">
                                <div class="accordion-body">
                                    KHCC AI Lab is a collaborative research initiative between 
                                    King Hussein Cancer Center and Princess Sumaya University for 
                                    Technology, focusing on developing AI solutions for healthcare, 
                                    particularly in cancer research and treatment.
                                </div>
                            </div>
                        </div>
                        
                        <div class="accordion-item border-0 shadow-sm mb-3">
                            <h3 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" 
                                        data-bs-toggle="collapse" 
                                        data-bs-target="#faq2">
                                    How can I get involved with the lab?
                                </button>
                            </h3>
                            <div id="faq2" class="accordion-collapse collapse" 
                                 data-bs-parent="#faqAccordion">
                                <div class="accordion-body">
                                    There are several ways to get involved:
                                    <ul>
                                        <li>Submit research proposals</li>
                                        <li>Apply for internships or research positions</li>
                                        <li>Collaborate on existing projects</li>
                                        <li>Attend our workshops and seminars</li>
                                    </ul>
                                    Contact us for more information about specific opportunities.
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Project Submission -->
                    <div class="mb-4">
                        <h2 class="h4 mb-3">Project Submission</h2>
                        
                        <div class="accordion-item border-0 shadow-sm mb-3">
                            <h3 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" 
                                        data-bs-toggle="collapse" 
                                        data-bs-target="#faq3">
                                    How do I submit a project?
                                </button>
                            </h3>
                            <div id="faq3" class="accordion-collapse collapse" 
                                 data-bs-parent="#faqAccordion">
                                <div class="accordion-body">
                                    To submit a project:
                                    <ol>
                                        <li>Create an account or sign in</li>
                                        <li>Click on "Submit Seed" in the navigation menu</li>
                                        <li>Fill out the project details form</li>
                                        <li>Include your GitHub repository link</li>
                                        <li>Add relevant tags</li>
                                        <li>Submit for review</li>
                                    </ol>
                                </div>
                            </div>
                        </div>
                        
                        <div class="accordion-item border-0 shadow-sm mb-3">
                            <h3 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" 
                                        data-bs-toggle="collapse" 
                                        data-bs-target="#faq4">
                                    What types of projects can I submit?
                                </button>
                            </h3>
                            <div id="faq4" class="accordion-collapse collapse" 
                                 data-bs-parent="#faqAccordion">
                                <div class="accordion-body">
                                    We accept projects related to:
                                    <ul>
                                        <li>Medical imaging and diagnosis</li>
                                        <li>Clinical data analysis</li>
                                        <li>Patient monitoring systems</li>
                                        <li>Drug discovery</li>
                                        <li>Healthcare process optimization</li>
                                        <li>Other healthcare-related AI applications</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Research & Collaboration -->
                    <div class="mb-4">
                        <h2 class="h4 mb-3">Research & Collaboration</h2>
                        
                        <div class="accordion-item border-0 shadow-sm mb-3">
                            <h3 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" 
                                        data-bs-toggle="collapse" 
                                        data-bs-target="#faq5">
                                    How can I collaborate with the lab?
                                </button>
                            </h3>
                            <div id="faq5" class="accordion-collapse collapse" 
                                 data-bs-parent="#faqAccordion">
                                <div class="accordion-body">
                                    We welcome collaborations from:
                                    <ul>
                                        <li>Academic researchers</li>
                                        <li>Healthcare professionals</li>
                                        <li>Industry partners</li>
                                        <li>Students</li>
                                    </ul>
                                    Contact our research team to discuss potential collaboration 
                                    opportunities.
                                </div>
                            </div>
                        </div>
                        
                        <div class="accordion-item border-0 shadow-sm mb-3">
                            <h3 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" 
                                        data-bs-toggle="collapse" 
                                        data-bs-target="#faq6">
                                    Do you offer research funding?
                                </button>
                            </h3>
                            <div id="faq6" class="accordion-collapse collapse" 
                                 data-bs-parent="#faqAccordion">
                                <div class="accordion-body">
                                    Yes, we offer research funding through various programs:
                                    <ul>
                                        <li>Graduate research fellowships</li>
                                        <li>Project-specific grants</li>
                                        <li>Collaborative research initiatives</li>
                                    </ul>
                                    Check our research page for current opportunities.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Contact Section -->
<section class="contact-section bg-light py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Still Have Questions?</h2>
                <p class="mb-4">
                    We're here to help! Feel free to reach out if you need any assistance 
                    or have questions not covered in our FAQ.
                </p>
                <div class="d-flex justify-content-center gap-3">
                    <a href="{% url 'contact' %}" class="btn btn-primary">
                        Contact Us
                    </a>
                    <a href="mailto:support@khccpsutailab.com" class="btn btn-outline-primary">
                        Email Support
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}

# Contents from: .\templates\projects\homepage.html
{% extends 'base.html' %}
{% load static %}
{% load humanize %}

{% block title %}KHCC AI Lab - Home{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="hero bg-primary text-white py-5 mb-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold mb-4">Welcome to KHCC AI Lab</h1>
                <p class="lead mb-4">
                    A collaborative platform for sharing and discovering innovative AI projects 
                    incubated @ King Hussein Cancer Center.
                </p>
                {% if not user.is_authenticated %}
                <div class="d-flex gap-3">
                    <a href="{% url 'account_signup' %}" class="btn btn-light btn-lg">
                        Join Now
                    </a>
                    <a href="{% url 'account_login' %}" class="btn btn-outline-light btn-lg">
                        Sign In
                    </a>
                </div>
                {% else %}
                <a href="{% url 'submit_project' %}" class="btn btn-light btn-lg">
                    Share Your Seed
                </a>
                {% endif %}
            </div>
            <div class="col-lg-6 d-none d-lg-block">
                <div class="text-center">
                    <img src="{% static 'images/collaboration.svg' %}" alt="Collaboration" class="img-fluid" style="max-height: 400px;">
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Featured Seeds Section -->
<section class="featured-projects mb-5">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="h3 mb-0">Featured Seeds</h2>
            <a href="{% url 'project_list' %}" class="btn btn-link text-decoration-none">
                View All Seeds <i class="bi bi-arrow-right"></i>
            </a>
        </div>
        
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            {% for project in featured_projects %}
            <div class="col">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex align-items-center mb-3">
                            <img src="{% if project.author.profile.avatar %}{{ project.author.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ project.author.username }}{% endif %}" 
                                 alt="{{ project.author.username }}" 
                                 class="rounded-circle me-2" 
                                 style="width: 32px; height: 32px;">
                            <div>
                                <a href="{% url 'user_profile' project.author.username %}" 
                                   class="text-decoration-none text-dark">{{ project.author.username }}</a>
                                <div class="text-muted small">{{ project.created_at|naturaltime }}</div>
                            </div>
                        </div>
                        
                        <h3 class="h5 card-title mb-3">
                            <a href="{% url 'project_detail' project.pk %}" 
                               class="text-decoration-none text-dark">{{ project.title }}</a>
                        </h3>
                        
                        <p class="card-text text-muted mb-3">
                            {{ project.description|truncatewords:30 }}
                        </p>
                        
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="d-flex gap-3">
                                <span title="Claps">
                                    <i class="bi bi-hand-thumbs-up"></i> {{ project.claps }}
                                </span>
                                <span title="Comments">
                                    <i class="bi bi-chat"></i> {{ project.comment_count }}
                                </span>
                            </div>
                            <div class="tag-cloud">
                                {% for tag in project.tag_list|slice:":3" %}
                                <span class="badge bg-light text-dark">{{ tag }}</span>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Latest Seeds Section -->
<section class="latest-projects bg-light py-5 mb-5">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="h3 mb-0">Latest Seeds</h2>
            <a href="{% url 'project_list' %}?sort=-created_at" class="btn btn-link text-decoration-none">
                View All <i class="bi bi-arrow-right"></i>
            </a>
        </div>
        
        <div class="row row-cols-1 row-cols-md-2 g-4">
            {% for project in latest_projects %}
            <div class="col">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body">
                        <h3 class="h5 card-title mb-3">
                            <a href="{% url 'project_detail' project.pk %}" 
                               class="text-decoration-none text-dark">{{ project.title }}</a>
                        </h3>
                        
                        <p class="card-text text-muted mb-3">
                            {{ project.description|truncatewords:20 }}
                        </p>
                        
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">{{ project.created_at|naturaltime }}</small>
                            <a href="{{ project.github_link }}" 
                               target="_blank" 
                               class="btn btn-sm btn-outline-dark">
                                <i class="bi bi-github"></i> View Code
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Statistics Section -->
<section class="statistics mb-5">
    <div class="container">
        <div class="row g-4">
            <div class="col-md-3">
                <div class="card border-0 shadow-sm text-center">
                    <div class="card-body">
                        <i class="bi bi-folder-fill display-4 text-primary mb-3"></i>
                        <h3 class="h4">{{ stats.total_projects }}</h3>
                        <p class="text-muted mb-0">Seeds Shared</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm text-center">
                    <div class="card-body">
                        <i class="bi bi-people-fill display-4 text-primary mb-3"></i>
                        <h3 class="h4">{{ stats.total_users }}</h3>
                        <p class="text-muted mb-0">Community Members</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm text-center">
                    <div class="card-body">
                        <i class="bi bi-chat-fill display-4 text-primary mb-3"></i>
                        <h3 class="h4">{{ stats.total_comments }}</h3>
                        <p class="text-muted mb-0">Comments Made</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm text-center">
                    <div class="card-body">
                        <i class="bi bi-hand-thumbs-up-fill display-4 text-primary mb-3"></i>
                        <h3 class="h4">{{ stats.total_claps }}</h3>
                        <p class="text-muted mb-0">Claps Given</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Partners Section -->
<section class="partners bg-light py-5 mb-5">
    <div class="container">
        <h2 class="h3 text-center mb-5">Our Partners</h2>
        <div class="row justify-content-center align-items-center">
            <div class="col-md-4 text-center mb-4 mb-md-0">
                <img src="{% static 'images/khcc-logo.png' %}" 
                     alt="King Hussein Cancer Center" 
                     class="img-fluid" 
                     style="max-height: 100px;">
            </div>
            <div class="col-md-4 text-center">
                <img src="{% static 'images/psut-logo.png' %}" 
                     alt="Princess Sumaya University for Technology" 
                     class="img-fluid" 
                     style="max-height: 100px;">
            </div>
        </div>
    </div>
</section>

<!-- Call to Action -->
<section class="cta mb-5">
    <div class="container">
        <div class="card border-0 bg-primary text-white shadow">
            <div class="card-body text-center py-5">
                <h2 class="h3 mb-4">Ready to Share Your AI Seed?</h2>
                <p class="lead mb-4">
                    Join our community of innovators and showcase your work to the world.
                </p>
                {% if user.is_authenticated %}
                <a href="{% url 'submit_project' %}" class="btn btn-light btn-lg">
                    Submit Your Seed
                </a>
                {% else %}
                <a href="{% url 'account_signup' %}" class="btn btn-light btn-lg">
                    Get Started
                </a>
                {% endif %}
            </div>
        </div>
    </div>
</section>
{% endblock %}

# Contents from: .\templates\projects\leaderboard.html
import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Star, Users, ChevronUp, ChevronDown } from 'lucide-react';

const LeaderboardCard = ({ rank, user, contributions, change }) => {
  return (
    <div className="flex items-center mb-4 p-4 bg-white rounded-lg shadow-sm">
      <div className={`flex items-center justify-center w-10 h-10 rounded-full mr-4 
        ${rank <= 3 ? 'bg-yellow-100' : 'bg-gray-100'}`}>
        <span className={`font-bold ${rank <= 3 ? 'text-yellow-600' : 'text-gray-600'}`}>
          {rank}
        </span>
      </div>
      
      <div className="flex-1">
        <div className="flex items-center">
          <h3 className="font-medium">{user}</h3>
          {rank <= 3 && <Star className="w-4 h-4 ml-2 text-yellow-500" />}
        </div>
        <div className="text-sm text-gray-600">
          {contributions} contributions
        </div>
      </div>
      
      <div className={`flex items-center ${change > 0 ? 'text-green-600' : 'text-red-600'}`}>
        {change > 0 ? (
          <ChevronUp className="w-4 h-4" />
        ) : (
          <ChevronDown className="w-4 h-4" />
        )}
        <span className="ml-1">{Math.abs(change)}</span>
      </div>
    </div>
  );
};

const LeaderboardComponent = () => {
  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader className="border-b">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-semibold">
            Monthly Contributions
          </CardTitle>
          <div className="flex items-center text-sm text-gray-600">
            <Users className="w-4 h-4 mr-2" />
            <span>Active Contributors: 142</span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-6">
        {/* Example leaderboard data */}
        {[
          { rank: 1, user: "Sarah Chen", contributions: 47, change: 5 },
          { rank: 2, user: "Alex Kim", contributions: 42, change: -2 },
          { rank: 3, user: "Maria Garcia", contributions: 38, change: 3 },
          { rank: 4, user: "John Smith", contributions: 35, change: 1 },
          { rank: 5, user: "David Lee", contributions: 31, change: -1 }
        ].map((entry) => (
          <LeaderboardCard key={entry.rank} {...entry} />
        ))}
        
        <div className="mt-6 text-center">
          <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
            View Full Leaderboard
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

export default LeaderboardComponent;

# Contents from: .\templates\projects\notification.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card shadow-sm">
                <div class="card-header bg-white d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Notifications</h5>
                    {% if notifications %}
                    <a href="?mark_read=true" class="btn btn-sm btn-outline-primary">
                        Mark all as read
                    </a>
                    {% endif %}
                </div>
                <div class="list-group list-group-flush">
                    {% for notification in notifications %}
                    <div class="list-group-item {% if not notification.is_read %}bg-light{% endif %}">
                        <div class="d-flex">
                            <img src="{% if notification.sender.profile.avatar %}{{ notification.sender.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ notification.sender.username }}{% endif %}" 
                                 class="rounded-circle me-3" 
                                 style="width: 40px; height: 40px; object-fit: cover;">
                            <div class="flex-grow-1">
                                <div class="d-flex justify-content-between align-items-center">
                                    <p class="mb-1">{{ notification.message }}</p>
                                    <small class="text-muted">{{ notification.created_at|timesince }} ago</small>
                                </div>
                                <div>
                                    <a href="{% url 'mark_notification_read' notification.id %}" 
                                       class="btn btn-sm btn-link px-0">
                                        View
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% empty %}
                    <div class="list-group-item text-center py-5">
                        <i class="bi bi-bell text-muted display-4"></i>
                        <p class="text-muted mt-3 mb-0">No notifications yet</p>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\templates\projects\profile_settings.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <!-- Sidebar -->
        <div class="col-md-3">
            <div class="card">
                <div class="list-group list-group-flush">
                    <a href="{% url 'projects:edit_profile' %}" 
                       class="list-group-item list-group-item-action {% if active_tab == 'profile' %}active{% endif %}">
                        <i class="bi bi-person"></i> Profile
                    </a>
                    <a href="{% url 'projects:profile_settings' %}" 
                       class="list-group-item list-group-item-action {% if active_tab == 'settings' %}active{% endif %}">
                        <i class="bi bi-gear"></i> Settings
                    </a>
                    <a href="{% url 'account_email' %}" 
                       class="list-group-item list-group-item-action">
                        <i class="bi bi-envelope"></i> Email
                    </a>
                    <a href="{% url 'account_change_password' %}" 
                       class="list-group-item list-group-item-action">
                        <i class="bi bi-shield-lock"></i> Password
                    </a>
                </div>
            </div>
        </div>

        <!-- Settings Form -->
        <div class="col-md-9">
            <div class="card">
                <div class="card-header">
                    <h4 class="card-title mb-0">Notification Settings</h4>
                </div>
                <div class="card-body">
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-{{ message.tags }}">
                                {{ message }}
                            </div>
                        {% endfor %}
                    {% endif %}

                    <form method="post">
                        {% csrf_token %}
                        {% for field in form %}
                            <div class="form-check mb-3">
                                {{ field }}
                                <label class="form-check-label" for="{{ field.id_for_label }}">
                                    {{ field.label }}
                                </label>
                            </div>
                        {% endfor %}
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\templates\projects\project_analytics.html
<!-- templates/projects/project_analytics.html -->
{% extends 'base.html' %}
{% load static %}
{% load humanize %}

{% block title %}Analytics for {{ project.title }} - KHCC AI Lab{% endblock %}

{% block extra_css %}
<style>
    .stat-card {
        transition: transform 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .chart-container {
        position: relative;
        height: 300px;
    }
    
    .percentage-circle {
        width: 120px;
        height: 120px;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .device-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid py-5">
    <div class="row justify-content-center">
        <div class="col-xxl-10">
            <!-- Header -->
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h1 class="h3 mb-2">Analytics for {{ project.title }}</h1>
                    <p class="text-muted mb-0">
                        Data from {{ analytics.created_at|date:"M d, Y" }} to {{ now|date:"M d, Y" }}
                    </p>
                </div>
                <div class="d-flex gap-2">
                    <div class="dropdown">
                        <button class="btn btn-light dropdown-toggle" 
                                type="button" 
                                data-bs-toggle="dropdown">
                            <i class="bi bi-download me-1"></i>Export
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li>
                                <a class="dropdown-item" href="#" onclick="exportToPDF()">
                                    <i class="bi bi-file-pdf me-2"></i>PDF Report
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="#" onclick="exportToCSV()">
                                    <i class="bi bi-file-excel me-2"></i>CSV Data
                                </a>
                            </li>
                        </ul>
                    </div>
                    <a href="{% url 'projects:project_detail' project.pk %}" 
                       class="btn btn-primary">
                        <i class="bi bi-arrow-left me-1"></i>Back to Project
                    </a>
                </div>
            </div>
            
            <!-- Overview Stats -->
            <div class="row g-4 mb-4">
                <div class="col-sm-6 col-xl-3">
                    <div class="card border-0 shadow-sm stat-card">
                        <div class="card-body">
                            <div class="d-flex align-items-center mb-3">
                                <div class="flex-shrink-0">
                                    <i class="bi bi-eye text-primary fs-1"></i>
                                </div>
                                <div class="flex-grow-1 ms-3">
                                    <h6 class="text-muted mb-1">Total Views</h6>
                                    <h3 class="mb-0">{{ analytics.view_count|intcomma }}</h3>
                                </div>
                            </div>
                            <div class="d-flex align-items-center">
                                {% if view_growth > 0 %}
                                <span class="badge bg-success me-2">
                                    <i class="bi bi-arrow-up me-1"></i>{{ view_growth }}%
                                </span>
                                {% else %}
                                <span class="badge bg-danger me-2">
                                    <i class="bi bi-arrow-down me-1"></i>{{ view_growth|abs }}%
                                </span>
                                {% endif %}
                                <small class="text-muted">vs. last month</small>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-sm-6 col-xl-3">
                    <div class="card border-0 shadow-sm stat-card">
                        <div class="card-body">
                            <div class="d-flex align-items-center mb-3">
                                <div class="flex-shrink-0">
                                    <i class="bi bi-people text-success fs-1"></i>
                                </div>
                                <div class="flex-grow-1 ms-3">
                                    <h6 class="text-muted mb-1">Unique Visitors</h6>
                                    <h3 class="mb-0">{{ analytics.unique_visitors|intcomma }}</h3>
                                </div>
                            </div>
                            <div class="progress" style="height: 4px;">
                                <div class="progress-bar bg-success" 
                                     role="progressbar" 
                                     style="width: {{ visitor_percentage }}%"></div>
                            </div>
                            <small class="text-muted">
                                {{ visitor_percentage }}% of total views
                            </small>
                        </div>
                    </div>
                </div>
                
                <div class="col-sm-6 col-xl-3">
                    <div class="card border-0 shadow-sm stat-card">
                        <div class="card-body">
                            <div class="d-flex align-items-center mb-3">
                                <div class="flex-shrink-0">
                                    <i class="bi bi-github text-dark fs-1"></i>
                                </div>
                                <div class="flex-grow-1 ms-3">
                                    <h6 class="text-muted mb-1">GitHub Clicks</h6>
                                    <h3 class="mb-0">{{ analytics.github_clicks|intcomma }}</h3>
                                </div>
                            </div>
                            <div class="d-flex align-items-center">
                                <div class="flex-grow-1">
                                    <div class="d-flex justify-content-between mb-1">
                                        <small>Click Rate</small>
                                        <small>{{ github_click_rate }}%</small>
                                    </div>
                                    <div class="progress" style="height: 4px;">
                                        <div class="progress-bar bg-dark" 
                                             style="width: {{ github_click_rate }}%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-sm-6 col-xl-3">
                    <div class="card border-0 shadow-sm stat-card">
                        <div class="card-body">
                            <div class="d-flex align-items-center mb-3">
                                <div class="flex-shrink-0">
                                    <i class="bi bi-clock-history text-info fs-1"></i>
                                </div>
                                <div class="flex-grow-1 ms-3">
                                    <h6 class="text-muted mb-1">Avg. Time Spent</h6>
                                    <h3 class="mb-0">{{ analytics.avg_time_spent|time:"i:s" }}</h3>
                                </div>
                            </div>
                            <small class="text-muted">
                                Based on {{ analytics.view_count }} pageviews
                            </small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Charts Row -->
            <div class="row g-4 mb-4">
                <!-- Traffic Over Time -->
                <div class="col-xl-8">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-header bg-transparent border-0">
                            <div class="d-flex justify-content-between align-items-center">
                                <h5 class="mb-0">Traffic Over Time</h5>
                                <div class="btn-group">
                                    <button type="button" 
                                            class="btn btn-sm btn-light active"
                                            data-time-range="week">
                                        Week
                                    </button>
                                    <button type="button" 
                                            class="btn btn-sm btn-light"
                                            data-time-range="month">
                                        Month
                                    </button>
                                    <button type="button" 
                                            class="btn btn-sm btn-light"
                                            data-time-range="year">
                                        Year
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="chart-container">
                                <canvas id="trafficChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Traffic Sources -->
                <div class="col-xl-4">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-header bg-transparent border-0">
                            <h5 class="mb-0">Traffic Sources</h5>
                        </div>
                        <div class="card-body">
                            <div class="chart-container">
                                <canvas id="sourcesChart"></canvas>
                            </div>
                            <div class="mt-4">
                                <div class="d-flex justify-content-between mb-2">
                                    <span class="d-flex align-items-center">
                                        <i class="bi bi-circle-fill text-primary me-2"></i>
                                        Direct
                                    </span>
                                    <span>{{ analytics.direct_traffic_percentage }}%</span>
                                </div>
                                <div class="d-flex justify-content-between mb-2">
                                    <span class="d-flex align-items-center">
                                        <i class="bi bi-circle-fill text-success me-2"></i>
                                        Social
                                    </span>
                                    <span>{{ analytics.social_traffic_percentage }}%</span>
                                </div>
                                <div class="d-flex justify-content-between mb-2">
                                    <span class="d-flex align-items-center">
                                        <i class="bi bi-circle-fill text-info me-2"></i>
                                        Search
                                    </span>
                                    <span>{{ analytics.search_traffic_percentage }}%</span>
                                </div>
                                <div class="d-flex justify-content-between">
                                    <span class="d-flex align-items-center">
                                        <i class="bi bi-circle-fill text-warning me-2"></i>
                                        Referral
                                    </span>
                                    <span>{{ analytics.referral_traffic_percentage }}%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Visitor Demographics -->
            <div class="row g-4 mb-4">
                <!-- Devices -->
                <div class="col-md-4">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-header bg-transparent border-0">
                            <h5 class="mb-0">Devices</h5>
                        </div>
                        <div class="card-body text-center">
                            <div class="row g-4">
                                <div class="col-4">
                                    <div class="device-stats">
                                        <i class="bi bi-laptop device-icon text-primary"></i>
                                        <h4 class="mb-1">{{ analytics.desktop_percentage }}%</h4>
                                        <div class="text-muted">Desktop</div>
                                    </div>
                                </div>
                                <div class="col-4">
                                    <div class="device-stats">
                                        <i class="bi bi-phone device-icon text-success"></i>
                                        <h4 class="mb-1">{{ analytics.mobile_percentage }}%</h4>
                                        <div class="text-muted">Mobile</div>
                                    </div>
                                </div>
                                <div class="col-4">
                                    <div class="device-stats">
                                        <i class="bi bi-tablet device-icon text-info"></i>
                                        <h4 class="mb-1">{{ analytics.tablet_percentage }}%</h4>
                                        <div class="text-muted">Tablet</div>
                                    </div>
                                </div>
                            </div>
                            <div class="chart-container mt-4">
                                <canvas id="devicesChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Browsers -->
                <div class="col-md-4">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-header bg-transparent border-0">
                            <h5 class="mb-0">Browsers</h5>
                        </div>
                        <div class="card-body">
                            <div class="chart-container">
                                <canvas id="browsersChart"></canvas>
                            </div>
                            <div class="mt-4">
                                {% for browser in browser_stats %}
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <div class="d-flex align-items-center">
                                        <i class="bi bi-{{ browser.icon }} me-2"></i>
                                        {{ browser.name }}
                                    </div>
                                    <div class="d-flex align-items-center">
                                        <div class="progress flex-grow-1 me-2" style="width: 100px; height: 4px;">
                                            <div class="progress-bar" 
                                                 style="width: {{ browser.percentage }}%; background-color: {{ browser.color }}">
                                            </div>
                                        </div>
                                        <span class="text-muted small">{{ browser.percentage }}%</span>
                                    </div>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Geographic Distribution -->
                <div class="col-md-4">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-header bg-transparent border-0">
                            <h5 class="mb-0">Geographic Distribution</h5>
                        </div>
                        <div class="card-body">
                            <div class="chart-container">
                                <canvas id="geoChart"></canvas>
                            </div>
                            <div class="mt-4">
                                {% for country in top_countries %}
                                <div class="d-flex justify-content-between mb-2">
                                    <span>{{ country.name }}</span>
                                    <span class="text-muted">{{ country.percentage }}%</span>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Engagement Metrics -->
            <div class="row g-4">
                <div class="col-md-6">
                    <div class="card border-0 shadow-sm">
                        <div class="card-header bg-transparent border-0">
                            <h5 class="mb-0">Engagement Metrics</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Metric</th>
                                            <th>Last 7 Days</th>
                                            <th>Last 30 Days</th>
                                            <th>Trend</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Comments</td>
                                            <td>{{ weekly_stats.comments }}</td>
                                            <td>{{ monthly_stats.comments }}</td>
                                            <td>
                                                {% if comment_trend > 0 %}
                                                <span class="text-success">
                                                    <i class="bi bi-arrow-up"></i> {{ comment_trend }}%
                                                </span>
                                                {% else %}
                                                <span class="text-danger">
                                                    <i class="bi bi-arrow-down"></i> {{ comment_trend|abs }}%
                                                </span>
                                                {% endif %}
                                            </td>
                                        </tr>
                                        <!-- Similar rows for claps, ratings, bookmarks -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card border-0 shadow-sm">
                        <div class="card-header bg-transparent border-0">
                            <h5 class="mb-0">Popular Referrers</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Source</th>
                                            <th>Visitors</th>
                                            <th>Conversion Rate</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for referrer in top_referrers %}
                                        <tr>
                                            <td>
                                                <div class="d-flex align-items-center">
                                                    <img src="{{ referrer.icon }}" 
                                                         alt="{{ referrer.name }}" 
                                                         width="16" 
                                                         height="16" 
                                                         class="me-2">
                                                    {{ referrer.name }}
                                                </div>
                                            </td>
                                            <td>{{ referrer.visitors }}</td>
                                            <td>
                                                <div class="d-flex align-items-center">
                                                    {{ referrer.conversion_rate }}%
                                                    <div class="progress ms-2" style="width: 50px; height: 4px;">
                                                        <div class="progress-bar" 
                                                             style="width: {{ referrer.conversion_rate }}%">
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Traffic Over Time Chart
    const trafficChart = new Chart(document.getElementById('trafficChart'), {
        type: 'line',
        data: {
            labels: {{ date_labels|safe }},
            datasets: [{
                label: 'Views',
                data: {{ view_data|safe }},
                borderColor: 'rgb(59, 130, 246)',
                tension: 0.4,
                fill: true,
                backgroundColor: 'rgba(59, 130, 246, 0.1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
    
    // Traffic Sources Chart
    const sourcesChart = new Chart(document.getElementById('sourcesChart'), {
        type: 'doughnut',
        data: {
            labels: ['Direct', 'Social', 'Search', 'Referral'],
            datasets: [{
                data: [
                    {{ analytics.direct_traffic }},
                    {{ analytics.social_traffic }},
                    {{ analytics.search_traffic }},
                    {{ analytics.referral_traffic }}
                ],
                backgroundColor: [
                    'rgb(59, 130, 246)',
                    'rgb(34, 197, 94)',
                    'rgb(14, 165, 233)',
                    'rgb(234, 179, 8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            cutout: '70%'
        }
    });
    
    // Initialize other charts similarly...
    
    // Export functions
    // Devices Chart
    const devicesChart = new Chart(document.getElementById('devicesChart'), {
        type: 'doughnut',
        data: {
            labels: ['Desktop', 'Mobile', 'Tablet'],
            datasets: [{
                data: [
                    {{ analytics.desktop_visits }},
                    {{ analytics.mobile_visits }},
                    {{ analytics.tablet_visits }}
                ],
                backgroundColor: [
                    'rgb(59, 130, 246)',
                    'rgb(34, 197, 94)',
                    'rgb(14, 165, 233)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            cutout: '60%'
        }
    });

    // Browsers Chart
    const browsersChart = new Chart(document.getElementById('browsersChart'), {
        type: 'bar',
        data: {
            labels: ['Chrome', 'Firefox', 'Safari', 'Edge', 'Other'],
            datasets: [{
                data: [
                    {{ analytics.chrome_visits }},
                    {{ analytics.firefox_visits }},
                    {{ analytics.safari_visits }},
                    {{ analytics.edge_visits }},
                    {{ analytics.other_browsers }}
                ],
                backgroundColor: [
                    'rgb(59, 130, 246)',
                    'rgb(245, 158, 11)',
                    'rgb(16, 185, 129)',
                    'rgb(99, 102, 241)',
                    'rgb(156, 163, 175)'
                ]
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });

    // Geographic Distribution Chart
    const geoChart = new Chart(document.getElementById('geoChart'), {
        type: 'pie',
        data: {
            labels: {{ geo_labels|safe }},
            datasets: [{
                data: {{ geo_data|safe }},
                backgroundColor: [
                    'rgb(59, 130, 246)',
                    'rgb(34, 197, 94)',
                    'rgb(14, 165, 233)',
                    'rgb(234, 179, 8)',
                    'rgb(156, 163, 175)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Time range selector functionality
    document.querySelectorAll('[data-time-range]').forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            document.querySelectorAll('[data-time-range]').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Update chart data based on selected range
            const range = this.dataset.timeRange;
            fetch(`{% url 'projects:analytics_data' project.pk %}?range=${range}`)
                .then(response => response.json())
                .then(data => {
                    trafficChart.data.labels = data.labels;
                    trafficChart.data.datasets[0].data = data.views;
                    trafficChart.update();
                });
        });
    });

    // Export functionality
    window.exportToPDF = function() {
        const loading = document.createElement('div');
        loading.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center bg-white bg-opacity-75';
        loading.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary mb-2" role="status"></div>
                <div>Generating PDF report...</div>
            </div>
        `;
        document.body.appendChild(loading);

        // Convert all charts to base64 images
        const chartImages = {
            traffic: trafficChart.toBase64Image(),
            sources: sourcesChart.toBase64Image(),
            devices: devicesChart.toBase64Image(),
            browsers: browsersChart.toBase64Image(),
            geo: geoChart.toBase64Image()
        };

        // Send data to backend for PDF generation
        fetch("{% url 'projects:export_analytics' project.pk %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({
                charts: chartImages,
                dateRange: document.querySelector('[data-time-range].active').dataset.timeRange
            })
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${project.title.toLowerCase().replace(/\s+/g, '-')}-analytics.pdf`;
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(loading);
        })
        .catch(error => {
            console.error('Error generating PDF:', error);
            document.body.removeChild(loading);
            alert('Error generating PDF report. Please try again.');
        });
    };

    window.exportToCSV = function() {
        const loading = document.createElement('div');
        loading.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center bg-white bg-opacity-75';
        loading.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary mb-2" role="status"></div>
                <div>Generating CSV export...</div>
            </div>
        `;
        document.body.appendChild(loading);

        fetch("{% url 'projects:export_analytics_csv' project.pk %}")
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${project.title.toLowerCase().replace(/\s+/g, '-')}-analytics.csv`;
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(loading);
            })
            .catch(error => {
                console.error('Error generating CSV:', error);
                document.body.removeChild(loading);
                alert('Error generating CSV export. Please try again.');
            });
    };

    // Update charts data periodically
    function updateCharts() {
        fetch(`{% url 'projects:analytics_data' project.pk %}`)
            .then(response => response.json())
            .then(data => {
                // Update traffic chart
                trafficChart.data.datasets[0].data = data.views;
                trafficChart.update();

                // Update other metrics
                Object.keys(data.metrics).forEach(key => {
                    const element = document.getElementById(key);
                    if (element) {
                        element.textContent = data.metrics[key];
                    }
                });
            });
    }

    // Update every 5 minutes
    setInterval(updateCharts, 300000);
});
</script>
{% endblock %}

# Contents from: .\templates\projects\project_detail.html
<!-- templates/projects/project_detail.html -->
{% extends 'base.html' %}
{% load static %}
{% load humanize %}
{% load crispy_forms_tags %}

{% block extra_css %}
<style>
    .featured-image {
        max-height: 500px;
        object-fit: cover;
        width: 100%;
    }
    
    .file-card {
        transition: transform 0.2s;
    }
    
    .file-card:hover {
        transform: translateY(-2px);
    }
    
    .comment-image {
        max-width: 300px;
        border-radius: 8px;
        cursor: pointer;
    }
    
    .file-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .tag-badge {
        transition: all 0.2s;
    }
    
    .tag-badge:hover {
        background-color: var(--bs-primary) !important;
        color: white !important;
    }
    
    .clap-button.active {
        animation: pulse 0.5s;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
</style>
{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <!-- Main Content Column -->
        <div class="col-lg-8">
            <!-- Project Header -->
            <div class="card shadow-sm mb-4">
                {% if project.featured_image %}
                <img src="{{ project.featured_image.url }}" 
                     alt="{{ project.title }}" 
                     class="featured-image card-img-top">
                {% endif %}
                
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-4">
                        <div>
                            <h1 class="h2 mb-3">{{ project.title }}</h1>
                            <div class="d-flex align-items-center mb-3">
                                <img src="{% if project.author.profile.avatar %}{{ project.author.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ project.author.username }}{% endif %}" 
                                     alt="{{ project.author.username }}" 
                                     class="rounded-circle me-2" 
                                     style="width: 40px; height: 40px; object-fit: cover;">
                                <div>
                                    <a href="{% url 'projects:user_profile' project.author.username %}" 
                                       class="text-decoration-none">
                                        {{ project.author.username }}
                                    </a>
                                    <div class="text-muted small">
                                        Posted {{ project.created_at|naturaltime }}
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        {% if user == project.author %}
                        <div class="dropdown">
                            <button class="btn btn-light btn-sm" type="button" data-bs-toggle="dropdown">
                                <i class="bi bi-three-dots-vertical"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li>
                                    <a href="{% url 'projects:edit_project' project.pk %}" 
                                       class="dropdown-item">
                                        <i class="bi bi-pencil me-2"></i>Edit Project
                                    </a>
                                </li>
                                <li>
                                    <a href="{% url 'projects:project_analytics' project.pk %}" 
                                       class="dropdown-item">
                                        <i class="bi bi-graph-up me-2"></i>View Analytics
                                    </a>
                                </li>
                                <li><hr class="dropdown-divider"></li>
                                <li>
                                    <button type="button" 
                                            class="dropdown-item text-danger" 
                                            data-bs-toggle="modal" 
                                            data-bs-target="#deleteProjectModal">
                                        <i class="bi bi-trash me-2"></i>Delete Project
                                    </button>
                                </li>
                            </ul>
                        </div>
                        {% endif %}
                    </div>
                    
                    <!-- Project Description -->
                    <div class="project-content mb-4">
                        {{ project.description|linebreaks }}
                    </div>
                    
                    <!-- Tags -->
                    <div class="mb-4">
                        {% for tag in project.tag_list %}
                        <a href="{% url 'projects:project_list' %}?tags={{ tag }}" 
                           class="badge bg-light text-dark text-decoration-none me-1 tag-badge">
                            {{ tag }}
                        </a>
                        {% endfor %}
                    </div>
                    
                    <!-- Project Files -->
                    {% if project.pdf_file or project.additional_files %}
                    <div class="row g-3 mb-4">
                        {% if project.pdf_file %}
                        <div class="col-md-6">
                            <div class="card h-100 file-card">
                                <div class="card-body text-center">
                                    <i class="bi bi-file-pdf text-danger file-icon"></i>
                                    <h5 class="card-title">Documentation</h5>
                                    <p class="text-muted small mb-3">
                                        PDF - {{ project.pdf_file.size|filesizeformat }}
                                    </p>
                                    <a href="{{ project.pdf_file.url }}" 
                                       class="btn btn-outline-primary btn-sm" 
                                       target="_blank">
                                        <i class="bi bi-download me-1"></i>Download
                                    </a>
                                </div>
                            </div>
                        </div>
                        {% endif %}
                        
                        {% if project.additional_files %}
                        <div class="col-md-6">
                            <div class="card h-100 file-card">
                                <div class="card-body text-center">
                                    <i class="bi bi-file-earmark-zip text-primary file-icon"></i>
                                    <h5 class="card-title">Additional Files</h5>
                                    <p class="text-muted small mb-3">
                                        {{ project.additional_files.name|split:'/'|last }}
                                        ({{ project.additional_files.size|filesizeformat }})
                                    </p>
                                    <a href="{{ project.additional_files.url }}" 
                                       class="btn btn-outline-primary btn-sm">
                                        <i class="bi bi-download me-1"></i>Download
                                    </a>
                                </div>
                            </div>
                        </div>
                        {% endif %}
                    </div>
                    {% endif %}
                    
                    <!-- Action Buttons -->
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex gap-2">
                            <a href="{{ project.github_link }}" 
                               target="_blank" 
                               class="btn btn-dark">
                                <i class="bi bi-github me-2"></i>View on GitHub
                            </a>
                            
                            {% if user.is_authenticated %}
                            <button id="clap-btn" 
                                    class="btn btn-outline-primary clap-button {% if user_has_clapped %}active{% endif %}"
                                    data-project-id="{{ project.id }}">
                                <i class="bi bi-hand-thumbs-up{% if user_has_clapped %}-fill{% endif %} me-1"></i>
                                <span id="clap-count">{{ project.claps }}</span>
                            </button>
                            
                            <button class="btn btn-outline-primary" 
                                    data-bs-toggle="modal" 
                                    data-bs-target="#ratingModal">
                                <i class="bi bi-star me-1"></i>Rate
                            </button>
                            
                            <button class="btn btn-outline-primary bookmark-btn" 
                                    data-project-id="{{ project.id }}"
                                    {% if user_bookmark %}data-bookmarked="true"{% endif %}>
                                <i class="bi bi-bookmark{% if user_bookmark %}-fill{% endif %}"></i>
                            </button>
                            {% endif %}
                        </div>
                        
                        <!-- Share Buttons -->
                        <div class="dropdown share-dropdown">
                            <button class="btn btn-outline-secondary dropdown-toggle" 
                                    type="button" 
                                    data-bs-toggle="dropdown">
                                <i class="bi bi-share me-1"></i>Share
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li>
                                    <a class="dropdown-item" href="https://twitter.com/intent/tweet?text={{ project.title|urlencode }}&url={{ request.build_absolute_uri|urlencode }}" target="_blank">
                                        <i class="bi bi-twitter me-2"></i>Twitter
                                    </a>
                                </li>
                                <li>
                                    <a class="dropdown-item" href="https://www.linkedin.com/shareArticle?mini=true&url={{ request.build_absolute_uri|urlencode }}&title={{ project.title|urlencode }}" target="_blank">
                                        <i class="bi bi-linkedin me-2"></i>LinkedIn
                                    </a>
                                </li>
                                <li>
                                    <button class="dropdown-item copy-link" data-url="{{ request.build_absolute_uri }}">
                                        <i class="bi bi-link-45deg me-2"></i>Copy Link
                                    </button>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Comments Section -->
            <div class="card shadow-sm">
                <div class="card-header bg-white">
                    <h4 class="card-title mb-0">Comments ({{ project.comments.count }})</h4>
                </div>
                <div class="card-body">
                    {% if user.is_authenticated %}
                    <form method="post" enctype="multipart/form-data" class="mb-4">
                        {% csrf_token %}
                        {{ comment_form|crispy }}
                        <div class="d-flex justify-content-between align-items-center mt-3">
                            <div class="form-text">
                                You can attach an image to your comment (optional)
                            </div>
                            <button type="submit" class="btn btn-primary">
                                Post Comment
                            </button>
                        </div>
                    </form>
                    {% else %}
                    <div class="alert alert-info">
                        Please <a href="{% url 'login' %}?next={{ request.path }}">sign in</a> 
                        to comment on this project.
                    </div>
                    {% endif %}
                    
                    <!-- Comments List -->
                    <div class="comments-list">
                        {% for comment in comments %}
                        <div class="comment-thread mb-4">
                            <!-- Parent Comment -->
                            <div class="card">
                                <div class="card-body">
                                    <div class="d-flex mb-3">
                                        <img src="{% if comment.user.profile.avatar %}{{ comment.user.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ comment.user.username }}{% endif %}" 
                                             alt="{{ comment.user.username }}" 
                                             class="rounded-circle me-2" 
                                             style="width: 32px; height: 32px;">
                                        <div>
                                            <h6 class="mb-0">{{ comment.user.username }}</h6>
                                            <small class="text-muted">
                                                {{ comment.created_at|naturaltime }}
                                            </small>
                                        </div>
                                    </div>
                                    
                                    <p class="mb-3">{{ comment.content }}</p>
                                    
                                    {% if comment.image %}
                                    <img src="{{ comment.image.url }}" 
                                         alt="Comment image" 
                                         class="comment-image mb-3"
                                         data-bs-toggle="modal"
                                         data-bs-target="#imageModal">
                                    {% endif %}
                                    
                                    {% if user.is_authenticated %}
                                    <div class="d-flex gap-2">
                                        <button class="btn btn-sm btn-light reply-btn" 
                                                data-comment-id="{{ comment.id }}">
                                            Reply
                                        </button>
                                        
                                        {% if user == comment.user or user == project.author %}
                                        <button class="btn btn-sm btn-light text-danger delete-comment-btn"
                                                data-comment-id="{{ comment.id }}">
                                            Delete
                                        </button>
                                        {% endif %}
                                    </div>
                                    {% endif %}
                                </div>
                            </div>
                            
                            <!-- Reply Form (hidden by default) -->
                            <div class="reply-form ms-4 mt-2" id="reply-form-{{ comment.id }}" style="display: none;">
                                <form method="post" enctype="multipart/form-data">
                                    {% csrf_token %}
                                    <input type="hidden" name="parent_id" value="{{ comment.id }}">
                                    {{ comment_form|crispy }}
                                    <div class="d-flex justify-content-end gap-2 mt-2">
                                        <button type="button" class="btn btn-light cancel-reply">
                                            Cancel
                                        </button>
                                        <button type="submit" class="btn btn-primary">
                                            Post Reply
                                        </button>
                                    </div>
                                </form>
                            </div>
                            
                            <!-- Replies -->
                            {% if comment.replies.exists %}
                            <div class="ms-4 mt-2">
                                {% for reply in comment.replies.all %}
                                <div class="card mb-2">
                                    <div class="card-body">
                                        <div class="d-flex mb-2">
                                            <img src="{% if reply.user.profile.avatar %}{{ reply.user.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ reply.user.username }}{% endif %}" 
                                                 alt="{{ reply.user.username }}" 
                                                 class="rounded-circle me-2" 
                                                 style="width: 24px; height: 24px;">
                                            <div>
                                                <h6 class="mb-0">{{ reply.user.username }}</h6>
                                                <small class="text-muted">
                                                    {{ reply.created_at|naturaltime }}
                                                </small>
                                            </div>
                                        </div>
                                        
                                        <p class="mb-2">{{ reply.content }}</p>
                                        
                                        {% if reply.image %}
                                        {% if reply.image %}
                                        <img src="{{ reply.image.url }}" 
                                             alt="Reply image" 
                                             class="comment-image mb-2"
                                             data-bs-toggle="modal"
                                             data-bs-target="#imageModal">
                                        {% endif %}
                                        
                                        {% if user == reply.user or user == project.author %}
                                        <button class="btn btn-sm btn-light text-danger delete-comment-btn"
                                                data-comment-id="{{ reply.id }}">
                                            Delete
                                        </button>
                                        {% endif %}
                                    </div>
                                </div>
                                {% endfor %}
                            </div>
                            {% endif %}
                        </div>
                        {% empty %}
                        <div class="text-center py-4">
                            <i class="bi bi-chat-dots text-muted display-4"></i>
                            <p class="text-muted mt-2">No comments yet. Be the first to share your thoughts!</p>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Sidebar -->
        <div class="col-lg-4">
            <!-- Project Stats -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <h5 class="card-title mb-4">Project Statistics</h5>
                    <div class="row g-3">
                        <div class="col-6">
                            <div class="d-flex align-items-center">
                                <i class="bi bi-hand-thumbs-up text-primary me-2"></i>
                                <div>
                                    <div class="small text-muted">Claps</div>
                                    <strong>{{ project.claps }}</strong>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="d-flex align-items-center">
                                <i class="bi bi-chat-dots text-primary me-2"></i>
                                <div>
                                    <div class="small text-muted">Comments</div>
                                    <strong>{{ project.comments.count }}</strong>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="d-flex align-items-center">
                                <i class="bi bi-star text-primary me-2"></i>
                                <div>
                                    <div class="small text-muted">Avg Rating</div>
                                    <strong>{{ project.average_rating|default:"No ratings" }}</strong>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="d-flex align-items-center">
                                <i class="bi bi-eye text-primary me-2"></i>
                                <div>
                                    <div class="small text-muted">Views</div>
                                    <strong>{{ project.view_count }}</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Author Card -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <h5 class="card-title mb-4">About the Author</h5>
                    <div class="d-flex align-items-center mb-3">
                        <img src="{% if project.author.profile.avatar %}{{ project.author.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ project.author.username }}{% endif %}" 
                             alt="{{ project.author.username }}" 
                             class="rounded-circle me-3" 
                             style="width: 64px; height: 64px; object-fit: cover;">
                        <div>
                            <h6 class="mb-1">{{ project.author.username }}</h6>
                            {% if project.author.profile.location %}
                            <p class="text-muted small mb-0">
                                <i class="bi bi-geo-alt me-1"></i>{{ project.author.profile.location }}
                            </p>
                            {% endif %}
                        </div>
                    </div>
                    
                    {% if project.author.profile.bio %}
                    <p class="small mb-3">{{ project.author.profile.bio }}</p>
                    {% endif %}
                    
                    <div class="d-flex gap-2 mb-3">
                        {% if project.author.profile.github_username %}
                        <a href="https://github.com/{{ project.author.profile.github_username }}" 
                           class="btn btn-sm btn-dark" 
                           target="_blank">
                            <i class="bi bi-github me-1"></i>GitHub
                        </a>
                        {% endif %}
                        
                        {% if project.author.profile.linkedin_url %}
                        <a href="{{ project.author.profile.linkedin_url }}" 
                           class="btn btn-sm btn-primary" 
                           target="_blank">
                            <i class="bi bi-linkedin me-1"></i>LinkedIn
                        </a>
                        {% endif %}
                    </div>
                    
                    <div class="d-flex justify-content-between text-muted small">
                        <span>Seeds: {{ project.author.projects.count }}</span>
                        <span>Joined: {{ project.author.date_joined|date:"M Y" }}</span>
                    </div>
                </div>
            </div>
            
            <!-- Similar Seeds -->
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="card-title mb-4">Similar Seeds</h5>
                    {% get_similar_projects project as similar_projects %}
                    {% for similar in similar_projects %}
                    <div class="mb-3">
                        <h6 class="mb-1">
                            <a href="{% url 'projects:project_detail' similar.pk %}" 
                               class="text-decoration-none">
                                {{ similar.title }}
                            </a>
                        </h6>
                        <p class="text-muted small mb-2">
                            {{ similar.description|truncatechars:100 }}
                        </p>
                        <div class="d-flex justify-content-between align-items-center small">
                            <span class="text-muted">
                                by {{ similar.author.username }}
                            </span>
                            <span class="text-muted">
                                {{ similar.created_at|naturaltime }}
                            </span>
                        </div>
                    </div>
                    {% if not forloop.last %}<hr class="my-3">{% endif %}
                    {% empty %}
                    <p class="text-muted text-center mb-0">No similar projects found</p>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modals -->
<!-- Rating Modal -->
<div class="modal fade" id="ratingModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Rate this Project</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form method="post" action="{% url 'projects:rate_project' project.pk %}">
                <div class="modal-body">
                    {% csrf_token %}
                    {{ rating_form|crispy }}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-light" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Submit Rating</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Image Modal -->
<div class="modal fade" id="imageModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-body p-0">
                <button type="button" class="btn-close position-absolute top-0 end-0 m-2" 
                        data-bs-dismiss="modal"></button>
                <img src="" class="img-fluid" id="modalImage">
            </div>
        </div>
    </div>
</div>

<!-- Delete Comment Modal -->
<div class="modal fade" id="deleteCommentModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Delete Comment</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to delete this comment? This action cannot be undone.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-light" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-danger" id="confirmDeleteComment">Delete</button>
            </div>
        </div>
    </div>
</div>

<!-- Delete Project Modal -->
<div class="modal fade" id="deleteProjectModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Delete Project</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to delete this project? This action cannot be undone.</p>
                <ul class="text-danger">
                    <li>All comments will be deleted</li>
                    <li>All files will be removed</li>
                    <li>All analytics data will be lost</li>
                </ul>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-light" data-bs-dismiss="modal">Cancel</button>
                <form method="post" action="{% url 'projects:delete_project' project.pk %}">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-danger">Delete Project</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
{{ block.super }}
<script>
$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Handle clap button
    $('#clap-btn').click(function() {
        const btn = $(this);
        $.post("{% url 'projects:clap_project' %}", {
            project_id: {{ project.id }},
            csrfmiddlewaretoken: '{{ csrf_token }}'
        })
        .done(function(response) {
            if (response.status === 'success') {
                $('#clap-count').text(response.claps);
                btn.toggleClass('active');
                btn.find('i').toggleClass('bi-hand-thumbs-up bi-hand-thumbs-up-fill');
            }
        });
    });
    
    // Handle reply buttons
    $('.reply-btn').click(function() {
        const commentId = $(this).data('comment-id');
        $('.reply-form').hide();
        $(`#reply-form-${commentId}`).show();
    });
    
    $('.cancel-reply').click(function() {
        $(this).closest('.reply-form').hide();
    });
    
    // Handle image modal
    $('.comment-image').click(function() {
        $('#modalImage').attr('src', $(this).attr('src'));
    });
    
    // Handle comment deletion
    let commentToDelete = null;
    
    $('.delete-comment-btn').click(function() {
        commentToDelete = $(this).data('comment-id');
        $('#deleteCommentModal').modal('show');
    });
    
    $('#confirmDeleteComment').click(function() {
        if (commentToDelete) {
            $.post("{% url 'projects:delete_comment' %}", {
                comment_id: commentToDelete,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            })
            .done(function() {
                location.reload();
            });
        }
    });
    
    // Handle bookmark toggle
    $('.bookmark-btn').click(function() {
        const btn = $(this);
        $.post("{% url 'projects:bookmark_project' project.pk %}", {
            csrfmiddlewaretoken: '{{ csrf_token }}'
        })
        .done(function(response) {
            if (response.status === 'success') {
                btn.find('i').toggleClass('bi-bookmark bi-bookmark-fill');
                const toast = new bootstrap.Toast($('#bookmarkToast'));
                $('#bookmarkMessage').text(response.message);
                toast.show();
            }
        });
    });
    
    // Handle share link copying
    $('.copy-link').click(function() {
        const url = $(this).data('url');
        navigator.clipboard.writeText(url).then(function() {
            const toast = new bootstrap.Toast($('#linkCopiedToast'));
            toast.show();
        });
    });
});
</script>
{% endblock %}

# Contents from: .\templates\projects\project_list.html
{% extends 'base.html' %}
{% load static %}
{% load crispy_forms_tags %}

{% block content %}
<div class="container py-5">
    <!-- Search Section -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-body">
                    <form method="get" class="row g-3">
                        <div class="col-md-4">
                            {{ search_form.query|as_crispy_field }}
                        </div>
                        <div class="col-md-4">
                            {{ search_form.tags|as_crispy_field }}
                        </div>
                        <div class="col-md-3">
                            {{ search_form.sort|as_crispy_field }}
                        </div>
                        <div class="col-md-1 d-flex align-items-end">
                            <button type="submit" class="btn btn-primary w-100">
                                <i class="bi bi-search"></i>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- Main Content -->
        <div class="col-lg-8">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2 class="h4 mb-0">Featured Seeds</h2>
                {% if user.is_authenticated %}
                <a href="{% url 'projects:submit_project' %}" class="btn btn-primary">
                    <i class="bi bi-plus-lg"></i> Share
                </a>
                {% endif %}
            </div>

            <div class="row row-cols-1 row-cols-md-2 g-4">
                {% for project in page_obj %}
                <div class="col">
                    <article class="card h-100 shadow-sm">
                        <div class="card-body">
                            <div class="d-flex align-items-center mb-3">
                                <img src="{% if project.author.profile.avatar %}{{ project.author.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ project.author.username }}{% endif %}" 
                                     alt="{{ project.author.username }}" 
                                     class="rounded-circle me-2" 
                                     style="width: 32px; height: 32px; object-fit: cover;">
                                <div>
                                    <a href="{% url 'projects:user_profile' project.author.username %}" 
                                       class="text-decoration-none text-dark">
                                        {{ project.author.username }}
                                    </a>
                                    <div class="text-muted small">
                                        {{ project.created_at|date:"M d, Y" }}
                                    </div>
                                </div>
                            </div>

                            <h3 class="h5 card-title mb-3">
                                <a href="{% url 'projects:project_detail' project.pk %}" 
                                   class="text-decoration-none text-dark">
                                    {{ project.title }}
                                </a>
                            </h3>

                            <p class="card-text text-muted mb-3">
                                {{ project.description|truncatewords:30 }}
                            </p>

                            <div class="tag-cloud mb-3">
                                {% for tag in project.tag_list %}
                                <a href="?tags={{ tag }}" 
                                   class="badge bg-light text-dark text-decoration-none me-1">
                                    {{ tag }}
                                </a>
                                {% endfor %}
                            </div>

                            <div class="d-flex justify-content-between align-items-center">
                                <div class="d-flex align-items-center">
                                    <span class="me-3" title="Claps">
                                        <i class="bi bi-hand-thumbs-up"></i>
                                        {{ project.claps }}
                                    </span>
                                    <span title="Comments">
                                        <i class="bi bi-chat"></i>
                                        {{ project.comment_count }}
                                    </span>
                                </div>
                                <a href="{{ project.github_link }}" 
                                   target="_blank" 
                                   class="btn btn-sm btn-outline-dark">
                                    <i class="bi bi-github"></i>
                                </a>
                            </div>
                        </div>
                    </article>
                </div>
                {% empty %}
                <div class="col-12">
                    <div class="text-center py-5">
                        <h3>No projects found</h3>
                        <p class="text-muted">Try adjusting your search criteria</p>
                        {% if user.is_authenticated %}
                        <a href="{% url 'projects:submit_project' %}" class="btn btn-primary">
                            Share Your Seed
                        </a>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>

            {% include "includes/pagination.html" %}
        </div>

        <!-- Sidebar -->
        <div class="col-lg-4">
            <!-- Welcome Card -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <h5 class="card-title">Welcome to KHCC AI Lab</h5>
                    <p class="card-text">
                        Discover innovative AI projects, share your work, and connect with 
                        fellow developers.
                    </p>
                    {% if user.is_authenticated %}
                    <a href="{% url 'projects:submit_project' %}" class="btn btn-primary w-100">
                        Share Your Seed
                    </a>
                    {% else %}
                    <a href="{% url 'account_login' %}" class="btn btn-primary w-100">
                        Sign in to Share
                    </a>
                    {% endif %}
                </div>
            </div>

            <!-- Popular Tags -->
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Popular Tags</h5>
                    <div class="tag-cloud">
                        {% for tag in popular_tags %}
                        <a href="?tags={{ tag.name }}" 
                           class="badge bg-light text-dark text-decoration-none">
                            {{ tag.name }}
                            <span class="text-muted">({{ tag.count }})</span>
                        </a>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\templates\projects\rateing_model.html
<!-- templates/projects/includes/rating_modal.html -->
<div class="modal fade" id="ratingModal" tabindex="-1" aria-labelledby="ratingModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="ratingModalLabel">Rate this project</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form id="ratingForm" method="post">
                <div class="modal-body">
                    {% csrf_token %}
                    <div class="rating-stars mb-3">
                        {% for value, label in rating_form.score.field.choices %}
                        <input type="radio" name="score" value="{{ value }}" id="star{{ value }}"
                               class="btn-check" autocomplete="off">
                        <label for="star{{ value }}" class="btn btn-outline-warning">
                            <i class="bi bi-star-fill"></i>
                        </label>
                        {% endfor %}
                    </div>
                    {{ rating_form.review|as_crispy_field }}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Submit Rating</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- templates/projects/bookmarks.html -->
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-8 mx-auto">
            <h2 class="mb-4">Your Bookmarks</h2>
            {% for bookmark in bookmarks %}
            <div class="card mb-3 shadow-sm">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <h5 class="card-title mb-3">
                            <a href="{% url 'project_detail' bookmark.project.pk %}" 
                               class="text-decoration-none text-dark">
                                {{ bookmark.project.title }}
                            </a>
                        </h5>
                        <button class="btn btn-sm btn-outline-danger remove-bookmark" 
                                data-project-id="{{ bookmark.project.pk }}">
                            <i class="bi bi-bookmark-x"></i>
                        </button>
                    </div>
                    
                    <p class="card-text text-muted mb-3">
                        {{ bookmark.project.description|truncatewords:30 }}
                    </p>
                    
                    <div class="mb-3">
                        <small class="text-muted">Bookmarked on: {{ bookmark.created_at|date }}</small>
                    </div>
                    
                    <form class="bookmark-notes-form">
                        <div class="form-group">
                            <label class="form-label">Your Notes:</label>
                            <textarea class="form-control" rows="2" 
                                      placeholder="Add personal notes about this project...">{{ bookmark.notes }}</textarea>
                        </div>
                        <button type="submit" class="btn btn-sm btn-primary mt-2">
                            Save Notes
                        </button>
                    </form>
                </div>
            </div>
            {% empty %}
            <div class="text-center py-5">
                <i class="bi bi-bookmark display-1 text-muted"></i>
                <h3 class="mt-3">No bookmarks yet</h3>
                <p class="text-muted">Start bookmarking projects you'd like to revisit later</p>
                <a href="{% url 'project_list' %}" class="btn btn-primary">
                    Browse Seeds
                </a>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}

<!-- templates/projects/analytics.html -->
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-10 mx-auto">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Analytics for {{ project.title }}</h2>
                <a href="{% url 'project_detail' project.pk %}" class="btn btn-outline-primary">
                    <i class="bi bi-arrow-left"></i> Back to Project
                </a>
            </div>
            
            <!-- Overview Cards -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h6 class="card-title">Total Views</h6>
                            <h2 class="mb-0">{{ analytics.view_count }}</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h6 class="card-title">Unique Visitors</h6>
                            <h2 class="mb-0">{{ analytics.unique_visitors }}</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h6 class="card-title">GitHub Clicks</h6>
                            <h2 class="mb-0">{{ analytics.github_clicks }}</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h6 class="card-title">Avg. Time Spent</h6>
                            <h2 class="mb-0">{{ analytics.avg_time_spent|time:"i:s" }}</h2>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Weekly vs Monthly Stats -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Last 7 Days</h5>
                        </div>
                        <div class="card-body">
                            <canvas id="weeklyChart"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Last 30 Days</h5>
                        </div>
                        <div class="card-body">
                            <canvas id="monthlyChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Engagement Metrics -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="card-title mb-0">User Engagement</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Metric</th>
                                            <th>Last 7 Days</th>
                                            <th>Last 30 Days</th>
                                            <th>Trend</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Comments</td>
                                            <td>{{ weekly_stats.comments }}</td>
                                            <td>{{ monthly_stats.comments }}</td>
                                            <td>
                                                {% if weekly_stats.comments > monthly_stats.comments %}
                                                <span class="text-success">
                                                    <i class="bi bi-arrow-up"></i>
                                                    {{ weekly_stats.comments|percentage:monthly_stats.comments }}%
                                                </span>
                                                {% else %}
                                                <span class="text-danger">
                                                    <i class="bi bi-arrow-down"></i>
                                                    {{ monthly_stats.comments|percentage:weekly_stats.comments }}%
                                                </span>
                                                {% endif %}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>Claps</td>
                                            <td>{{ weekly_stats.claps }}</td>
                                            <td>{{ monthly_stats.claps }}</td>
                                            <td>
                                                {% if weekly_stats.claps > monthly_stats.claps %}
                                                <span class="text-success">
                                                    <i class="bi bi-arrow-up"></i>
                                                    {{ weekly_stats.claps|percentage:monthly_stats.claps }}%
                                                </span>
                                                {% else %}
                                                <span class="text-danger">
                                                    <i class="bi bi-arrow-down"></i>
                                                    {{ monthly_stats.claps|percentage:weekly_stats.claps }}%
                                                </span>
                                                {% endif %}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>Ratings</td>
                                            <td>{{ weekly_stats.ratings }}</td>
                                            <td>{{ monthly_stats.ratings }}</td>
                                            <td>
                                                {% if weekly_stats.ratings > monthly_stats.ratings %}
                                                <span class="text-success">
                                                    <i class="bi bi-arrow-up"></i>
                                                    {{ weekly_stats.ratings|percentage:monthly_stats.ratings }}%
                                                </span>
                                                {% else %}
                                                <span class="text-danger">
                                                    <i class="bi bi-arrow-down"></i>
                                                    {{ monthly_stats.ratings|percentage:weekly_stats.ratings }}%
                                                </span>
                                                {% endif %}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>Bookmarks</td>
                                            <td>{{ weekly_stats.bookmarks }}</td>
                                            <td>{{ monthly_stats.bookmarks }}</td>
                                            <td>
                                                {% if weekly_stats.bookmarks > monthly_stats.bookmarks %}
                                                <span class="text-success">
                                                    <i class="bi bi-arrow-up"></i>
                                                    {{ weekly_stats.bookmarks|percentage:monthly_stats.bookmarks }}%
                                                </span>
                                                {% else %}
                                                <span class="text-danger">
                                                    <i class="bi bi-arrow-down"></i>
                                                    {{ monthly_stats.bookmarks|percentage:weekly_stats.bookmarks }}%
                                                </span>
                                                {% endif %}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Traffic Sources</h5>
                        </div>
                        <div class="card-body">
                            <canvas id="trafficSourcesChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Visitor Demographics -->
            <div class="row mb-4">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Visitor Demographics</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-4">
                                    <canvas id="locationChart"></canvas>
                                </div>
                                <div class="col-md-4">
                                    <canvas id="deviceChart"></canvas>
                                </div>
                                <div class="col-md-4">
                                    <canvas id="browserChart"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Weekly Stats Chart
    new Chart(document.getElementById('weeklyChart'), {
        type: 'line',
        data: {
            labels: {{ weekly_labels|safe }},
            datasets: [{
                label: 'Views',
                data: {{ weekly_views|safe }},
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Daily Views (Last 7 Days)'
                }
            }
        }
    });

    // Monthly Stats Chart
    new Chart(document.getElementById('monthlyChart'), {
        type: 'line',
        data: {
            labels: {{ monthly_labels|safe }},
            datasets: [{
                label: 'Views',
                data: {{ monthly_views|safe }},
                borderColor: 'rgb(153, 102, 255)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Daily Views (Last 30 Days)'
                }
            }
        }
    });

    // Traffic Sources Chart
    new Chart(document.getElementById('trafficSourcesChart'), {
        type: 'doughnut',
        data: {
            labels: ['Direct', 'Social', 'Search', 'Referral'],
            datasets: [{
                data: {{ traffic_sources|safe }},
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });

    // Demographics Charts
    const demographicsOptions = {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    };

    new Chart(document.getElementById('locationChart'), {
        type: 'pie',
        data: {
            labels: {{ locations|safe }},
            datasets: [{
                data: {{ location_data|safe }},
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(153, 102, 255)'
                ]
            }]
        },
        options: demographicsOptions
    });

    new Chart(document.getElementById('deviceChart'), {
        type: 'pie',
        data: {
            labels: ['Desktop', 'Mobile', 'Tablet'],
            datasets: [{
                data: {{ device_data|safe }},
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ]
            }]
        },
        options: demographicsOptions
    });

    new Chart(document.getElementById('browserChart'), {
        type: 'pie',
        data: {
            labels: ['Chrome', 'Firefox', 'Safari', 'Edge', 'Other'],
            datasets: [{
                data: {{ browser_data|safe }},
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(153, 102, 255)'
                ]
            }]
        },
        options: demographicsOptions
    });
});
</script>
{% endblock %}

# Contents from: .\templates\projects\search.html
<!-- templates/projects/search.html -->
{% extends 'base.html' %}
{% load static %}
{% load crispy_forms_tags %}

{% block title %}Search Seeds - {{ block.super }}{% endblock %}

{% block extra_css %}
<link href="https://cdn.jsdelivr.net/npm/bootstrap-tagsinput@0.7.1/dist/bootstrap-tagsinput.css" rel="stylesheet">
<style>
    .bootstrap-tagsinput {
        width: 100%;
        padding: 0.375rem 0.75rem;
        font-size: 1rem;
        line-height: 1.5;
        color: #212529;
        background-color: #fff;
        border: 1px solid #ced4da;
        border-radius: 0.25rem;
        transition: border-color .15s ease-in-out,box-shadow .15s ease-in-out;
    }
    
    .bootstrap-tagsinput input {
        width: auto;
        max-width: inherit;
    }
    
    .filter-card {
        position: sticky;
        top: 20px;
    }
    
    .search-result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
    }
    
    .animated-loading {
        position: relative;
        overflow: hidden;
    }
    
    .animated-loading::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: loading 1.5s infinite;
    }
    
    @keyframes loading {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
</style>
{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <!-- Search Filters -->
        <div class="col-lg-3">
            <div class="card shadow-sm filter-card">
                <div class="card-body">
                    <h5 class="card-title mb-4">Search Filters</h5>
                    
                    <form method="get" id="searchForm" hx-get="{% url 'search_projects' %}" 
                          hx-target="#searchResults" hx-push-url="true" hx-indicator="#loading">
                        
                        <!-- Search Query -->
                        <div class="mb-3">
                            {{ form.query|as_crispy_field }}
                        </div>
                        
                        <!-- Tags -->
                        <div class="mb-3">
                            {{ form.tags|as_crispy_field }}
                        </div>
                        
                        <!-- Date Range -->
                        <div class="mb-3">
                            <label class="form-label">Date Range</label>
                            <div class="row g-2">
                                <div class="col">
                                    {{ form.date_from|as_crispy_field }}
                                </div>
                                <div class="col">
                                    {{ form.date_to|as_crispy_field }}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Minimum Claps -->
                        <div class="mb-3">
                            {{ form.min_claps|as_crispy_field }}
                        </div>
                        
                        <!-- Has GitHub -->
                        <div class="mb-3">
                            <div class="form-check">
                                {{ form.has_github }}
                                <label class="form-check-label" for="{{ form.has_github.id_for_label }}">
                                    Has GitHub Repository
                                </label>
                            </div>
                        </div>
                        
                        <!-- Sort By -->
                        <div class="mb-4">
                            {{ form.sort_by|as_crispy_field }}
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">
                                Apply Filters
                            </button>
                            <button type="button" class="btn btn-link" onclick="resetFilters()">
                                Reset Filters
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <!-- Search Results -->
        <div class="col-lg-9">
            <div id="searchResults">
                {% include 'projects/includes/project_list_results.html' %}
            </div>
        </div>
    </div>
</div>

<!-- Loading Indicator -->
<div id="loading" class="position-fixed top-50 start-50 translate-middle bg-white p-4 rounded shadow-lg d-none">
    <div class="d-flex align-items-center">
        <div class="spinner-border text-primary me-3" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <span>Loading results...</span>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/bootstrap-tagsinput@0.7.1/dist/bootstrap-tagsinput.min.js"></script>
<script src="https://unpkg.com/htmx.org@1.9.0"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tagsinput
    $('#id_tags').tagsinput({
        trimValue: true,
        confirmKeys: [13, 44], // Enter and comma
        maxTags: 5
    });
    
    // Auto-submit form on filter changes
    const form = document.getElementById('searchForm');
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('change', () => {
            form.requestSubmit();
        });
    });
});

function resetFilters() {
    const form = document.getElementById('searchForm');
    form.reset();
    $('#id_tags').tagsinput('removeAll');
    form.requestSubmit();
}
</script>
{% endblock %}

<!-- templates/projects/includes/project_list_results.html -->
{% load humanize %}

<div class="d-flex justify-content-between align-items-center mb-4">
    <h4 class="mb-0">
        Search Results 
        <small class="text-muted">({{ total_results }} projects found)</small>
    </h4>
    {% if form.is_valid and form.cleaned_data.query %}
    <p class="mb-0">
        Showing results for: <strong>{{ form.cleaned_data.query }}</strong>
    </p>
    {% endif %}
</div>

{% if projects %}
<div class="row row-cols-1 row-cols-md-2 g-4" id="projectGrid">
    {% for project in projects %}
    <div class="col">
        <div class="card h-100 border-0 shadow-sm search-result-card">
            <div class="card-body">
                <!-- Author Info -->
                <div class="d-flex align-items-center mb-3">
                    <img src="{% if project.author.profile.avatar %}{{ project.author.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ project.author.username }}{% endif %}" 
                         alt="{{ project.author.username }}" 
                         class="rounded-circle me-2" 
                         style="width: 32px; height: 32px;">
                    <div>
                        <a href="{% url 'user_profile' project.author.username %}" 
                           class="text-decoration-none text-dark">
                            {{ project.author.username }}
                        </a>
                        <div class="text-muted small">
                            {{ project.created_at|naturaltime }}
                        </div>
                    </div>
                </div>
                
                <!-- Project Title -->
                <h5 class="card-title mb-3">
                    <a href="{% url 'project_detail' project.pk %}" 
                       class="text-decoration-none text-dark">
                        {{ project.title }}
                    </a>
                </h5>
                
                <!-- Project Description -->
                <p class="card-text text-muted mb-3">
                    {{ project.description|truncatewords:30 }}
                </p>
                
                <!-- Tags -->
                <div class="mb-3">
                    {% for tag in project.tag_list %}
                    <a href="?tags={{ tag }}" 
                       class="badge bg-light text-dark text-decoration-none me-1">
                        {{ tag }}
                    </a>
                    {% endfor %}
                </div>
                
                <!-- Project Metrics -->
                <div class="d-flex justify-content-between align-items-center">
                    <div class="d-flex align-items-center gap-3">
                        <!-- Claps -->
                        <span class="text-muted" title="Claps">
                            <i class="bi bi-hand-thumbs-up"></i>
                            {{ project.claps }}
                        </span>
                        
                        <!-- Comments -->
                        <span class="text-muted" title="Comments">
                            <i class="bi bi-chat"></i>
                            {{ project.comment_count }}
                        </span>
                        
                        <!-- Average Rating -->
                        {% if project.rating_avg %}
                        <span class="text-muted" title="Average Rating">
                            <i class="bi bi-star-fill"></i>
                            {{ project.rating_avg|floatformat:1 }}
                        </span>
                        {% endif %}
                    </div>
                    
                    <!-- GitHub Link -->
                    <a href="{{ project.github_link }}" 
                       target="_blank" 
                       class="btn btn-sm btn-outline-dark">
                        <i class="bi bi-github"></i> View Code
                    </a>
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
</div>

<!-- Pagination -->
{% if projects.has_other_pages %}
<nav aria-label="Search results pagination" class="my-4">
    <ul class="pagination justify-content-center">
        {% if projects.has_previous %}
        <li class="page-item">
            <a class="page-link" 
               href="?{{ request.GET.urlencode }}&page={{ projects.previous_page_number }}"
               hx-get="?{{ request.GET.urlencode }}&page={{ projects.previous_page_number }}"
               hx-target="#searchResults"
               hx-push-url="true">
                Previous
            </a>
        </li>
        {% endif %}
        
        {% for num in projects.paginator.page_range %}
            {% if projects.number == num %}
            <li class="page-item active">
                <span class="page-link">{{ num }}</span>
            </li>
            {% elif num > projects.number|add:'-3' and num < projects.number|add:'3' %}
            <li class="page-item">
                <a class="page-link" 
                   href="?{{ request.GET.urlencode }}&page={{ num }}"
                   hx-get="?{{ request.GET.urlencode }}&page={{ num }}"
                   hx-target="#searchResults"
                   hx-push-url="true">
                    {{ num }}
                </a>
            </li>
            {% endif %}
        {% endfor %}
        
        {% if projects.has_next %}
        <li class="page-item">
            <a class="page-link" 
               href="?{{ request.GET.urlencode }}&page={{ projects.next_page_number }}"
               hx-get="?{{ request.GET.urlencode }}&page={{ projects.next_page_number }}"
               hx-target="#searchResults"
               hx-push-url="true">
                Next
            </a>
        </li>
        {% endif %}
    </ul>
</nav>
{% endif %}

{% else %}
<!-- No Results -->
<div class="text-center py-5">
    <i class="bi bi-search display-1 text-muted mb-3"></i>
    <h3>No projects found</h3>
    <p class="text-muted mb-4">
        Try adjusting your search criteria or explore some suggestions below.
    </p>
    
    {% if popular_tags %}
    <div class="mb-4">
        <h5 class="mb-3">Popular Tags</h5>
        <div class="d-flex justify-content-center flex-wrap gap-2">
            {% for tag in popular_tags %}
            <a href="?tags={{ tag.name }}" 
               class="badge bg-light text-dark text-decoration-none">
                {{ tag.name }}
                <span class="text-muted">({{ tag.count }})</span>
            </a>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    
    <a href="{% url 'project_list' %}" class="btn btn-primary">
        Browse All Seeds
    </a>
</div>
{% endif %}
                    

# Contents from: .\templates\projects\social_sharing.html
{% block content %}
<!-- Add this where appropriate in your project_detail.html -->
<div class="social-share my-4">
    <h6 class="text-muted mb-3">Share this project</h6>
    <div class="d-flex gap-2">
        <!-- Twitter -->
        <a href="https://twitter.com/intent/tweet?text={{ project.title|urlencode }}&url={{ request.build_absolute_uri|urlencode }}"
           target="_blank"
           class="btn btn-outline-primary">
            <i class="bi bi-twitter"></i>
        </a>
        
        <!-- LinkedIn -->
        <a href="https://www.linkedin.com/shareArticle?mini=true&url={{ request.build_absolute_uri|urlencode }}&title={{ project.title|urlencode }}&summary={{ project.description|truncatewords:30|urlencode }}"
           target="_blank"
           class="btn btn-outline-primary">
            <i class="bi bi-linkedin"></i>
        </a>
        
        <!-- Facebook -->
        <a href="https://www.facebook.com/sharer/sharer.php?u={{ request.build_absolute_uri|urlencode }}"
           target="_blank"
           class="btn btn-outline-primary">
            <i class="bi bi-facebook"></i>
        </a>
        
        <!-- Copy Link -->
        <button class="btn btn-outline-primary copy-link" 
                data-url="{{ request.build_absolute_uri }}">
            <i class="bi bi-link-45deg"></i>
        </button>
    </div>
</div>

{% block extra_js %}
{{ block.super }}
<script>
$(document).ready(function() {
    $('.copy-link').click(function() {
        const url = $(this).data('url');
        navigator.clipboard.writeText(url).then(function() {
            // Show success toast
            const toast = new bootstrap.Toast($('#copy-toast'));
            toast.show();
        });
    });
});
</script>
{% endblock %}

# Contents from: .\templates\projects\submit_project.html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h2 class="card-title mb-4">Share Your Seed</h2>
                    
                    <form method="post" class="mb-4">
                        {% csrf_token %}
                        {{ form|crispy }}
                        
                        <!-- Preview Section -->
                        <div class="card mt-4">
                            <div class="card-header">
                                Preview
                            </div>
                            <div class="card-body">
                                <div class="preview-content">
                                    <h3 id="preview-title">Seed title will appear here...</h3>
                                    <p id="preview-description" class="text-muted">Project description will appear here...</p>
                                    <div id="preview-tags" class="tag-cloud"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="d-grid gap-2 mt-4">
                            <button type="submit" class="btn btn-primary">
                                Submit Seed
                            </button>
                            <a href="{% url 'projects:project_list' %}" class="btn btn-outline-secondary">
                                Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Live preview functionality
    document.addEventListener('DOMContentLoaded', function() {
        const titleInput = document.getElementById('id_title');
        const descInput = document.getElementById('id_description');
        const tagsInput = document.getElementById('id_tags');
        
        const previewTitle = document.getElementById('preview-title');
        const previewDesc = document.getElementById('preview-description');
        const previewTags = document.getElementById('preview-tags');
        
        function updatePreview() {
            previewTitle.textContent = titleInput.value || 'Seed title will appear here...';
            previewDesc.textContent = descInput.value || 'Project description will appear here...';
            
            // Update tags
            const tags = tagsInput.value.split(',').map(tag => tag.trim()).filter(tag => tag);
            previewTags.innerHTML = tags.map(tag => 
                `<span class="badge bg-light text-dark me-1">${tag}</span>`
            ).join('');
        }
        
        titleInput.addEventListener('input', updatePreview);
        descInput.addEventListener('input', updatePreview);
        tagsInput.addEventListener('input', updatePreview);
    });
</script>
{% endblock %}

# Contents from: .\templates\projects\user_profile.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <!-- Profile Info -->
        <div class="col-md-4">
            <div class="card shadow-sm">
                <div class="card-body text-center">
                    <img src="{% if profile_user.profile.avatar %}{{ profile_user.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ profile_user.username }}{% endif %}" 
                         alt="{{ profile_user.username }}" 
                         class="rounded-circle mb-3" 
                         style="width: 150px; height: 150px; object-fit: cover;">
                    
                    <h4 class="card-title">{{ profile_user.username }}</h4>
                    {% if profile_user.profile.bio %}
                        <p class="text-muted">{{ profile_user.profile.bio }}</p>
                    {% endif %}
                    
                    <div class="d-flex justify-content-center gap-3 mb-3">
                        <div class="text-center">
                            <h6 class="mb-0">{{ projects.count }}</h6>
                            <small class="text-muted">Seeds</small>
                        </div>
                        <div class="text-center">
                            <h6 class="mb-0">{{ followers_count }}</h6>
                            <small class="text-muted">Followers</small>
                        </div>
                        <div class="text-center">
                            <h6 class="mb-0">{{ following_count }}</h6>
                            <small class="text-muted">Following</small>
                        </div>
                    </div>
                    
                    {% if user != profile_user %}
                        {% if user.is_authenticated %}
                            {% if is_following %}
                                <form action="{% url 'projects:unfollow_user' profile_user.username %}" method="post" class="d-inline">
                                    {% csrf_token %}
                                    <button type="submit" class="btn btn-outline-primary">Unfollow</button>
                                </form>
                            {% else %}
                                <form action="{% url 'projects:follow_user' profile_user.username %}" method="post" class="d-inline">
                                    {% csrf_token %}
                                    <button type="submit" class="btn btn-primary">Follow</button>
                                </form>
                            {% endif %}
                        {% endif %}
                    {% endif %}
                </div>
            </div>
        </div>
        
        <!-- Seeds -->
        <div class="col-md-8">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h4 class="mb-0">Seeds</h4>
                {% if user == profile_user %}
                    <a href="{% url 'projects:submit_project' %}" class="btn btn-primary btn-sm">
                        New Seed
                    </a>
                {% endif %}
            </div>
            
            {% for project in projects %}
                <div class="card border-0 shadow-sm mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3">
                            <a href="{% url 'projects:project_detail' project.pk %}" 
                               class="text-decoration-none text-dark">
                                {{ project.title }}
                            </a>
                        </h5>
                        
                        <p class="card-text text-muted">
                            {{ project.description|truncatewords:30 }}
                        </p>
                        
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="small text-muted">
                                <i class="bi bi-calendar"></i> {{ project.created_at|date:"M d, Y" }}
                                <i class="bi bi-hand-thumbs-up ms-3"></i> {{ project.claps }}
                                <i class="bi bi-chat ms-3"></i> {{ project.comments.count }}
                            </div>
                            <div>
                                {% for tag in project.tag_list %}
                                    <span class="badge bg-light text-dark">{{ tag }}</span>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                </div>
            {% empty %}
                <div class="text-center text-muted py-5">
                    <i class="bi bi-folder2-open display-4"></i>
                    <p class="mt-3">No projects yet</p>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\templates\registration\login.html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h2 class="card-title text-center mb-4">Sign In</h2>
                    <form method="post">
                        {% csrf_token %}
                        {{ form|crispy }}
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">Sign In</button>
                        </div>
                        <div class="text-center mt-3">
                            <a href="{% url 'auth:password_reset' %}">Forgot Password?</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\templates\registration\register.html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h2 class="card-title text-center mb-4">Sign Up</h2>
                    <form method="post">
                        {% csrf_token %}
                        {{ form|crispy }}
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">Sign Up</button>
                        </div>
                        <div class="text-center mt-3">
                            Already have an account? <a href="{% url 'login' %}">Sign In</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\static\js\search.js
// static/js/search.js

document.addEventListener('DOMContentLoaded', function() {
    // Initialize popovers
    const popoverTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Debounce function for search input
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Handle search input
    const searchInput = document.getElementById('id_query');
    if (searchInput) {
        const debouncedSearch = debounce(() => {
            document.getElementById('searchForm').requestSubmit();
        }, 500);
        
        searchInput.addEventListener('input', debouncedSearch);
    }
    
    // Handle tag clicks
    document.querySelectorAll('.tag-badge').forEach(tag => {
        tag.addEventListener('click', (e) => {
            e.preventDefault();
            const tagInput = document.getElementById('id_tags');
            const tagsinput = $(tagInput).tagsinput('items');
            const tagValue = e.target.dataset.tag;
            
            if (!tagsinput.includes(tagValue)) {
                $(tagInput).tagsinput('add', tagValue);
                document.getElementById('searchForm').requestSubmit();
            }
        });
    });
    
    // Handle sort changes
    const sortSelect = document.getElementById('id_sort_by');
    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            document.getElementById('searchForm').requestSubmit();
        });
    }
    
    // Initialize date range picker
    const dateFrom = document.getElementById('id_date_from');
    const dateTo = document.getElementById('id_date_to');
    
    if (dateFrom && dateTo) {
        dateFrom.addEventListener('change', () => {
            dateTo.min = dateFrom.value;
            document.getElementById('searchForm').requestSubmit();
        });
        
        dateTo.addEventListener('change', () => {
            dateFrom.max = dateTo.value;
            document.getElementById('searchForm').requestSubmit();
        });
    }
    
    // Handle filter reset
    document.getElementById('resetFilters')?.addEventListener('click', () => {
        const form = document.getElementById('searchForm');
        form.reset();
        $('#id_tags').tagsinput('removeAll');
        form.requestSubmit();
    });
    
    // Save search preferences
    function saveSearchPreferences() {
        const preferences = {
            sort_by: document.getElementById('id_sort_by').value,
            results_per_page: document.getElementById('id_results_per_page').value
        };
        localStorage.setItem('searchPreferences', JSON.stringify(preferences));
    }
    
    // Load search preferences
    function loadSearchPreferences() {
        const preferences = JSON.parse(
            localStorage.getItem('searchPreferences')
        );
        if (preferences) {
            document.getElementById('id_sort_by').value = 
                preferences.sort_by || '-created_at';
            document.getElementById('id_results_per_page').value = 
                preferences.results_per_page || '12';
        }
    }
    
    // Initialize preferences
    loadSearchPreferences();
    
    // Save preferences on change
    document.getElementById('id_sort_by')?.addEventListener('change', 
        saveSearchPreferences);
    document.getElementById('id_results_per_page')?.addEventListener('change', 
        saveSearchPreferences);
});

// HTMX after swap handling
document.body.addEventListener('htmx:afterSwap', function(evt) {
    // Reinitialize popovers after content update
    const popoverTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Smooth scroll to top of results on page change
    if (evt.detail.target.id === 'searchResults') {
        evt.detail.target.scrollIntoView({ behavior: 'smooth' });
    }
});

# Contents from: .\accounts\__init__.py


# Contents from: .\accounts\admin.py
from django.contrib import admin

# Register your models here.


# Contents from: .\accounts\apps.py
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"


# Contents from: .\accounts\migrations\__init__.py


# Contents from: .\accounts\models.py
from django.db import models

# Create your models here.


# Contents from: .\accounts\tests.py
from django.test import TestCase

# Create your tests here.


# Contents from: .\accounts\views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


# Contents from: .\combine.py
import os

def get_files_recursively(directory, extensions):
    """
    Recursively get all files with specified extensions from directory and subdirectories.
    Uses os.walk() to traverse through all subdirectories at any depth.
    Excludes any directories named 'migrations'.
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        # Exclude 'migrations' folders from the search
        dirs[:] = [d for d in dirs if d != '.venv']
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_list.append(os.path.join(root, file))
    return file_list

def combine_files(output_file, file_list):
    """
    Combine contents of all files in file_list into output_file
    """
    with open(output_file, 'a', encoding='utf-8') as outfile:
        for fname in file_list:
            # Add a header comment to show which file's contents follow
            outfile.write(f"\n\n# Contents from: {fname}\n")
            try:
                with open(fname, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        outfile.write(line)
            except Exception as e:
                outfile.write(f"# Error reading file {fname}: {str(e)}\n")

def main():
    # Define the base directory (current directory in this case)
    base_directory = "."
    output_file = 'combined.py'
    extensions = ('.py', '.html', '.css', '.js')

    # Remove output file if it exists
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except Exception as e:
            print(f"Error removing existing {output_file}: {str(e)}")
            return

    # Get all files recursively - os.walk() will traverse through all subdirectories
    all_files = get_files_recursively(base_directory, extensions)
    
    # Sort files by extension and then by name
    all_files.sort(key=lambda x: (os.path.splitext(x)[1], x))

    # Add a header to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("# Combined Python and HTML files\n")
        outfile.write(f"# Generated from directory: {os.path.abspath(base_directory)}\n")
        outfile.write(f"# Total files found: {len(all_files)}\n\n")

    # Combine all files
    combine_files(output_file, all_files)
    
    print(f"Successfully combined {len(all_files)} files into {output_file}")
    print("Files processed:")
    for file in all_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()

# Contents from: .\khcc_psut_ai_lab\__init__.py


# Contents from: .\khcc_psut_ai_lab\asgi.py
"""
ASGI config for khcc_psut_ai_lab project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "khcc_psut_ai_lab.settings")

application = get_asgi_application()


# Contents from: .\khcc_psut_ai_lab\settings.py
# khcc_psut_ai_lab/settings.py

from pathlib import Path
import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-b3(9-x8ohz16r#18d&b^sr&49e=@c6107rcyfq!h!4%7n=b@#!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Site specific settings
SITE_NAME = 'KHCC AI Lab'
SITE_URL = 'http://localhost:8000'  # Change this in production
ADMIN_EMAIL = 'admin@khccpsutailab.com'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    'projects.apps.ProjectsConfig',
    'accounts.apps.AccountsConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_bootstrap5',

    'rest_framework',
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


# Crispy Forms Settings
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Message tags
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Change based on your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-email@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-app-specific-password')
DEFAULT_FROM_EMAIL = f'{SITE_NAME} <{EMAIL_HOST_USER}>'

# For development, you can use console email backend
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# django-allauth settings
SITE_ID = 1
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'projects:project_list'
LOGOUT_REDIRECT_URL = 'account_login'
ACCOUNT_LOGOUT_REDIRECT_URL = 'home'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Options: 'none', 'optional', 'mandatory'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'administrator', 'staff', 'support']

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = "khcc_psut_ai_lab.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "projects.context_processors.site_context",  # Custom context processor
                'projects.context_processors.notifications_processor',
            ],
        },
    },
]

WSGI_APPLICATION = "khcc_psut_ai_lab.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        }
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# GitHub OAuth settings
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': os.environ.get('GITHUB_CLIENT_ID', 'your-github-client-id'),
            'secret': os.environ.get('GITHUB_CLIENT_SECRET', 'your-github-client-secret'),
            'key': ''
        },
        'SCOPE': [
            'read:user',
            'user:email',
        ],
    }
}

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644

# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_SECURE = not DEBUG

# Security settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Custom settings for the project
PROJECT_CLAP_COOLDOWN = 300  # 5 minutes between claps
MAX_TAGS_PER_PROJECT = 5
MAX_PROJECTS_PER_PAGE = 12
COMMENT_MAX_LENGTH = 1000
PROJECT_DESCRIPTION_MAX_LENGTH = 5000

# Django AllAuth Settings
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'projects:project_list'
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'

# New rate limiting configuration
ACCOUNT_RATE_LIMITS = {
    # Five failed login attempts in 5 minutes
    "login_failed": "5/5m",
    
    # Three email sends in 1 hour
    "email": "3/h",
    
    # Five password reset attempts in 1 hour
    "password_reset": "5/h",
    
    # Two password reset attempts from same IP in 1 hour
    "password_reset_ip": "2/h",
    
    # Five signup attempts from same IP in 1 day
    "signup_ip": "5/d",
}

# Authentication settings
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'projects:project_list'
LOGOUT_REDIRECT_URL = 'account_login'

# Django AllAuth settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

# Email settings (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Media and Static files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Contents from: .\khcc_psut_ai_lab\urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),
    
    # Django AllAuth URLs (preferred way)
    path('accounts/', include('allauth.urls')),
    
    # Optional: Custom auth views if needed
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='account/password_change.html'
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='account/password_change_done.html'
    ), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'
    ), name='password_reset_complete'),
] 

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'projects.views.custom_404'
handler500 = 'projects.views.custom_500'


# Contents from: .\khcc_psut_ai_lab\wsgi.py
"""
WSGI config for khcc_psut_ai_lab project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "khcc_psut_ai_lab.settings")

application = get_wsgi_application()


# Contents from: .\manage.py
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "khcc_psut_ai_lab.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()


# Contents from: .\projects\__init__.py


# Contents from: .\projects\admin.py
# projects/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from django.utils.safestring import mark_safe
from .models import (
    Project, Comment, Clap, UserProfile, Rating,
    Bookmark, ProjectAnalytics, Notification
)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author_link', 'created_at', 'claps_count',
        'comments_count', 'ratings_count', 'github_link_display'
    ]
    list_filter = ['created_at', 'author', 'tags']
    search_fields = ['title', 'description', 'author__username', 'tags']
    readonly_fields = ['created_at', 'updated_at', 'slug', 'claps']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'description', 'github_link', 'tags')
        }),
        ('Author Information', {
            'fields': ('author',)
        }),
        ('Metrics', {
            'fields': ('claps',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def author_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.username)
    author_link.short_description = 'Author'
    
    def claps_count(self, obj):
        return obj.claps
    claps_count.short_description = 'Claps'
    
    def comments_count(self, obj):
        count = obj.comments.count()
        url = reverse('admin:projects_comment_changelist')
        return format_html('<a href="{}?project__id={}">{}</a>', url, obj.id, count)
    comments_count.short_description = 'Comments'
    
    def ratings_count(self, obj):
        count = obj.ratings.count()
        url = reverse('admin:projects_rating_changelist')
        return format_html('<a href="{}?project__id={}">{}</a>', url, obj.id, count)
    ratings_count.short_description = 'Ratings'
    
    def github_link_display(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', 
                         obj.github_link, obj.github_link)
    github_link_display.short_description = 'GitHub Repository'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'user_link', 'project_link', 'parent_comment',
        'created_at', 'content_preview', 'has_replies'
    ]
    list_filter = ['created_at', 'user', 'project']
    search_fields = ['content', 'user__username', 'project__title']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def project_link(self, obj):
        url = reverse('admin:projects_project_change', args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', url, obj.project.title)
    project_link.short_description = 'Project'
    
    def parent_comment(self, obj):
        if obj.parent:
            return format_html('Reply to: {}', obj.parent.content[:50])
        return '-'
    parent_comment.short_description = 'Parent Comment'
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'
    
    def has_replies(self, obj):
        count = obj.replies.count()
        if count:
            url = reverse('admin:projects_comment_changelist')
            return format_html('<a href="{}?parent__id={}">{} replies</a>', 
                             url, obj.id, count)
        return 'No replies'
    has_replies.short_description = 'Replies'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user_link', 'location', 'github_username',
        'project_count', 'total_claps_received', 'avatar_preview'
    ]
    list_filter = ['location', 'created_at']
    search_fields = ['user__username', 'bio', 'location', 'github_username']
    readonly_fields = [
        'created_at', 'updated_at', 'avatar_preview',
        'project_count', 'total_claps_received'
    ]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'avatar', 'avatar_preview', 'bio')
        }),
        ('Contact Information', {
            'fields': ('location', 'website')
        }),
        ('Social Links', {
            'fields': ('github_username', 'linkedin_url')
        }),
        ('Statistics', {
            'fields': ('project_count', 'total_claps_received'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.avatar.url
            )
        return 'No avatar'
    avatar_preview.short_description = 'Avatar Preview'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'recipient_link', 'sender_link', 'notification_type',
        'is_read', 'created_at', 'message_preview'
    ]
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = [
        'recipient__username', 'sender__username',
        'message', 'project__title'
    ]
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def recipient_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.recipient.id])
        return format_html('<a href="{}">{}</a>', url, obj.recipient.username)
    recipient_link.short_description = 'Recipient'
    
    def sender_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.sender.id])
        return format_html('<a href="{}">{}</a>', url, obj.sender.username)
    sender_link.short_description = 'Sender'
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Message'
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected notifications as unread"

@admin.register(ProjectAnalytics)
class ProjectAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        'project_link', 'view_count', 'unique_visitors',
        'github_clicks', 'last_updated'
    ]
    list_filter = ['last_updated']
    readonly_fields = [
        'view_count', 'unique_visitors', 'github_clicks',
        'avg_time_spent', 'direct_traffic', 'social_traffic',
        'search_traffic', 'referral_traffic', 'desktop_visits',
        'mobile_visits', 'tablet_visits', 'chrome_visits',
        'firefox_visits', 'safari_visits', 'edge_visits',
        'other_browsers', 'unique_visitors_weekly',
        'unique_visitors_monthly', 'github_clicks_weekly',
        'github_clicks_monthly', 'last_updated'
    ]
    
    fieldsets = (
        ('Project Information', {
            'fields': ('project',)
        }),
        ('Basic Metrics', {
            'fields': (
                'view_count', 'unique_visitors',
                'github_clicks', 'avg_time_spent'
            )
        }),
        ('Traffic Sources', {
            'fields': (
                'direct_traffic', 'social_traffic',
                'search_traffic', 'referral_traffic'
            ),
            'classes': ('collapse',)
        }),
        ('Device Statistics', {
            'fields': (
                'desktop_visits', 'mobile_visits',
                'tablet_visits'
            ),
            'classes': ('collapse',)
        }),
        ('Browser Statistics', {
            'fields': (
                'chrome_visits', 'firefox_visits',
                'safari_visits', 'edge_visits',
                'other_browsers'
            ),
            'classes': ('collapse',)
        }),
        ('Time-based Metrics', {
            'fields': (
                'unique_visitors_weekly',
                'unique_visitors_monthly',
                'github_clicks_weekly',
                'github_clicks_monthly'
            ),
            'classes': ('collapse',)
        })
    )
    
    def project_link(self, obj):
        url = reverse('admin:projects_project_change', args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', url, obj.project.title)
    project_link.short_description = 'Project'

class CustomAdminSite(admin.AdminSite):
    site_header = 'KHCC AI Lab Administration'
    site_title = 'KHCC AI Lab Admin'
    index_title = 'Dashboard'
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        # Add custom statistics to the admin index
        app_list.append({
            'name': 'Statistics',
            'app_label': 'statistics',
            'models': [
                {
                    'name': 'Total Seeds',
                    'object_name': 'projects',
                    'count': Project.objects.count(),
                    'admin_url': reverse('admin:projects_project_changelist'),
                },
                {
                    'name': 'Total Users',
                    'object_name': 'users',
                    'count': UserProfile.objects.count(),
                    'admin_url': reverse('admin:auth_user_changelist'),
                },
                {
                    'name': 'Total Comments',
                    'object_name': 'comments',
                    'count': Comment.objects.count(),
                    'admin_url': reverse('admin:projects_comment_changelist'),
                },
                {
                    'name': 'Total Claps',
                    'object_name': 'claps',
                    'count': Clap.objects.count(),
                    'admin_url': '#',
                },
            ]
        })
        
        return app_list

# Register the custom admin site
admin_site = CustomAdminSite(name='admin')
admin_site.register(Project, ProjectAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(UserProfile, UserProfileAdmin)
admin_site.register(Notification, NotificationAdmin)
admin_site.register(ProjectAnalytics, ProjectAnalyticsAdmin)

# Contents from: .\projects\apps.py
from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "projects"


# Contents from: .\projects\context_processors.py
# projects/context_processors.py

from django.conf import settings
from .models import Project, UserProfile

def site_context(request):
    """
    Add common context variables to all templates
    """
    context = {
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
    }
    
    if request.user.is_authenticated:
        # Get unread notifications count
        context['unread_notifications_count'] = request.user.notifications.filter(
            is_read=False
        ).count()
        
        # Get user's bookmarked projects
        context['bookmarked_projects'] = Project.objects.filter(
            bookmarks__user=request.user
        ).values_list('id', flat=True)
        
        # Check if user has completed their profile
        try:
            profile = request.user.profile
            context['profile_completed'] = all([
                profile.bio,
                profile.location,
                profile.avatar
            ])
        except UserProfile.DoesNotExist:
            context['profile_completed'] = False
    
    return context

def notifications_processor(request):
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
        recent_notifications = request.user.notifications.all()[:5]
        return {
            'unread_notifications_count': unread_count,
            'notifications': recent_notifications,
        }
    return {}

# Contents from: .\projects\filters\__init__.py
from .project_filters import ProjectFilter

__all__ = ['ProjectFilter']


# Contents from: .\projects\filters\project_filters.py
import django_filters
from django.db.models import Q
from ..models import Project

class ProjectFilter(django_filters.FilterSet):
    """FilterSet for advanced project filtering"""
    query = django_filters.CharFilter(method='filter_query')
    tags = django_filters.CharFilter(method='filter_tags')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    min_claps = django_filters.NumberFilter(field_name='claps', lookup_expr='gte')
    has_github = django_filters.BooleanFilter(method='filter_has_github')
    
    class Meta:
        model = Project
        fields = ['query', 'tags', 'date_from', 'date_to', 'min_claps', 'has_github']
    
    def filter_query(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(author__username__icontains=value) |
            Q(tags__icontains=value)
        )
    
    def filter_tags(self, queryset, name, value):
        if not value:
            return queryset
        
        tags = [tag.strip().lower() for tag in value.split(',') if tag.strip()]
        for tag in tags:
            queryset = queryset.filter(tags__icontains=tag)
        return queryset
    
    def filter_has_github(self, queryset, name, value):
        if value:
            return queryset.exclude(github_link='')
        return queryset

# Contents from: .\projects\forms.py
# projects/forms.py

from django import forms
from django.core.validators import URLValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count, Q
import mimetypes
from PIL import Image
from io import BytesIO
import os

from .models import (
    Project,
    Comment,
    UserProfile,
    Rating,
    Bookmark,
    ProjectAnalytics,
    Notification,
    Profile
)

class ProjectForm(forms.ModelForm):
    """
    Form for creating and editing projects.
    Includes validation for GitHub links and tag formatting.
    """
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., AI, Machine Learning, NLP)',
            'data-toggle': 'tooltip',
            'title': 'Add up to 5 tags to help others find your project'
        })
    )
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_link', 'tags', 'pdf_file', 'featured_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title',
                'maxlength': '200',
                'data-toggle': 'tooltip',
                'title': 'Choose a descriptive title for your project'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your project in detail...',
                'data-toggle': 'tooltip',
                'title': 'Explain what your project does, technologies used, and its purpose'
            }),
            'github_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/repository',
                'data-toggle': 'tooltip',
                'title': 'Link to your GitHub repository'
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf',
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            })
        }

    def clean_github_link(self):
        """Validate GitHub repository URL"""
        url = self.cleaned_data['github_link']
        if not url.startswith(('https://github.com/', 'http://github.com/')):
            raise ValidationError('Please enter a valid GitHub repository URL')
        
        try:
            URLValidator()(url)
        except ValidationError:
            raise ValidationError('Please enter a valid URL')
        
        return url

    def clean_tags(self):
        """Validate and format tags"""
        tags = self.cleaned_data['tags']
        if not tags:
            return ''
        
        # Clean and validate tags
        tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = [x for x in tag_list if not (x in seen or seen.add(x))]
        
        if len(unique_tags) > 5:
            raise ValidationError('Please enter no more than 5 unique tags')
        
        if any(len(tag) > 20 for tag in unique_tags):
            raise ValidationError('Each tag must be less than 20 characters')
        
        return ', '.join(unique_tags)

    def clean_pdf_file(self):
        """Validate PDF file"""
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            # Check file size (10MB limit)
            if pdf_file.size > 10 * 1024 * 1024:
                raise ValidationError('PDF file must be smaller than 10MB')

            # Check file extension
            ext = os.path.splitext(pdf_file.name)[1].lower()
            if ext != '.pdf':
                raise ValidationError('Only PDF files are allowed')

            # Check MIME type using mimetypes
            file_type, encoding = mimetypes.guess_type(pdf_file.name)
            if file_type != 'application/pdf':
                raise ValidationError('Invalid PDF file')

        return pdf_file

    def clean_featured_image(self):
        """Validate and process featured image"""
        image = self.cleaned_data.get('featured_image')
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Image file must be smaller than 5MB')

            try:
                img = Image.open(image)
                
                # Convert to RGB if necessary
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Check dimensions
                if img.width > 2000 or img.height > 2000:
                    raise ValidationError('Image dimensions should not exceed 2000x2000 pixels')
                
                # Resize if larger than 1200px
                if img.width > 1200 or img.height > 1200:
                    output_size = (1200, 1200)
                    img.thumbnail(output_size, Image.LANCZOS)
                
                # Save optimized image
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                # Return processed image
                from django.core.files.uploadedfile import InMemoryUploadedFile
                return InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{os.path.splitext(image.name)[0]}.jpg",
                    'image/jpeg',
                    output.tell(),
                    None
                )
            except Exception as e:
                raise ValidationError(f'Invalid image file: {str(e)}')
        return image

class CommentForm(forms.ModelForm):
    """
    Form for adding comments to projects.
    Includes validation for minimum content length.
    """
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...',
                'data-toggle': 'tooltip',
                'title': 'Share your thoughts, feedback, or questions'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_content(self):
        """Validate comment content"""
        content = self.cleaned_data['content'].strip()
        if len(content) < 10:
            raise ValidationError('Comment must be at least 10 characters long')
        if len(content) > 1000:
            raise ValidationError('Comment must be less than 1000 characters')
        return content

    def clean_image(self):
        """Validate comment image"""
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (2MB limit)
            if image.size > 2 * 1024 * 1024:
                raise ValidationError('Image file must be smaller than 2MB')

            try:
                img = Image.open(image)
                
                # Convert to RGB if necessary
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Check dimensions
                if img.width > 1000 or img.height > 1000:
                    raise ValidationError('Image dimensions should not exceed 1000x1000 pixels')
                
                # Resize if larger than 800px
                if img.width > 800 or img.height > 800:
                    output_size = (800, 800)
                    img.thumbnail(output_size, Image.LANCZOS)
                
                # Save optimized image
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                # Return processed image
                from django.core.files.uploadedfile import InMemoryUploadedFile
                return InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{os.path.splitext(image.name)[0]}.jpg",
                    'image/jpeg',
                    output.tell(),
                    None
                )
            except Exception as e:
                raise ValidationError(f'Invalid image file: {str(e)}')
        return image

class UserProfileForm(forms.ModelForm):
    """Form for user profile management"""
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'website', 'github_username', 'linkedin_url', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
                'maxlength': '500'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where are you based?',
                'maxlength': '100'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourwebsite.com'
            }),
            'github_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your GitHub username',
                'maxlength': '39'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.linkedin.com/in/your-profile'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_avatar(self):
        """Validate avatar file"""
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Check file size (5MB limit)
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError('Avatar file must be smaller than 5MB')

            try:
                img = Image.open(avatar)
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Resize to standard avatar size
                output_size = (300, 300)
                img.thumbnail(output_size, Image.LANCZOS)
                
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                from django.core.files.uploadedfile import InMemoryUploadedFile
                return InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{os.path.splitext(avatar.name)[0]}.jpg",
                    'image/jpeg',
                    output.tell(),
                    None
                )
            except Exception as e:
                raise ValidationError(f'Invalid image file: {str(e)}')
        return avatar

class RatingForm(forms.ModelForm):
    """Form for rating projects"""
    class Meta:
        model = Rating
        fields = ['score', 'review']
        widgets = {
            'score': forms.Select(attrs={
                'class': 'form-select',
                'aria-label': 'Rating score'
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your experience with this project (optional)',
                'maxlength': 500
            })
        }

    def clean_review(self):
        review = self.cleaned_data.get('review', '').strip()
        if len(review) > 500:
            raise ValidationError('Review must be less than 500 characters')
        return review

class BookmarkForm(forms.ModelForm):
    """Form for managing bookmarks"""
    class Meta:
        model = Bookmark
        fields = ['project']
        widgets = {
            'project': forms.HiddenInput()
        }

class ProjectSearchForm(forms.Form):
    """Form for project search and filtering"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search seeds...',
            'aria-label': 'Search'
        })
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by tags (comma separated)',
            'aria-label': 'Tags'
        })
    )
    
    SORT_CHOICES = [
        ('-created_at', 'Newest first'),
        ('created_at', 'Oldest first'),
        ('-claps', 'Most popular'),
        ('title', 'Alphabetical'),
    ]
    
    sort = forms.ChoiceField(
        required=False,
        initial='-created_at',
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'aria-label': 'Sort projects'
        })
    )

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            return [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        return []
    

################################

class FileValidationMixin:
    """Mixin for common file validation methods"""
    
    def validate_file_size(self, file, max_size_mb=5):
        if file.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f'File size must be no more than {max_size_mb}MB')
    
    def validate_file_type(self, file, allowed_types):
        file_type = mimetypes.guess_type(file.name)[0]
        if file_type not in allowed_types:
            raise ValidationError(f'File type {file_type} is not supported')
    
    def validate_image(self, image, max_dimension=2000):
        try:
            img = Image.open(image)
            if img.width > max_dimension or img.height > max_dimension:
                raise ValidationError(f'Image dimensions should not exceed {max_dimension}x{max_dimension} pixels')
            return img
        except Exception as e:
            raise ValidationError(f'Invalid image file: {str(e)}')

class AdvancedSearchForm(forms.Form):
    """Advanced search form with multiple filters"""
    
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, description, or author'
        })
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'data-role': 'tagsinput'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    min_claps = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    has_github = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Newest first'),
            ('created_at', 'Oldest first'),
            ('-claps', 'Most popular'),
            ('-comment_count', 'Most discussed'),
            ('title', 'Alphabetical'),
            ('-rating_avg', 'Highest rated')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise ValidationError("End date should be greater than start date")
        
        return cleaned_data

# projects/filters.py

import django_filters
from django.db.models import Avg, Count, Q
from .models import Project

class ProjectFilter(django_filters.FilterSet):
    """FilterSet for advanced project filtering"""
    query = django_filters.CharFilter(method='filter_query')
    tags = django_filters.CharFilter(method='filter_tags')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    min_claps = django_filters.NumberFilter(field_name='claps', lookup_expr='gte')
    has_github = django_filters.BooleanFilter(method='filter_has_github')
    
    class Meta:
        model = Project
        fields = ['query', 'tags', 'date_from', 'date_to', 'min_claps', 'has_github']
    
    def filter_query(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(author__username__icontains=value) |
            Q(tags__icontains=value)
        )
    
    def filter_tags(self, queryset, name, value):
        if not value:
            return queryset
        
        tags = [tag.strip().lower() for tag in value.split(',') if tag.strip()]
        for tag in tags:
            queryset = queryset.filter(tags__icontains=tag)
        return queryset
    
    def filter_has_github(self, queryset, name, value):
        if value:
            return queryset.exclude(github_link='')
        return queryset

# Now let's update the views.py to use these filters:

class NotificationSettingsForm(forms.Form):
    email_on_comment = forms.BooleanField(
        required=False,
        label='Email me when someone comments on my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    email_on_follow = forms.BooleanField(
        required=False,
        label='Email me when someone follows me',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    email_on_clap = forms.BooleanField(
        required=False,
        label='Email me when someone claps for my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    email_on_bookmark = forms.BooleanField(
        required=False,
        label='Email me when someone bookmarks my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = Profile
        fields = [
            'bio', 
            'location', 
            'website', 
            'github_username', 
            'twitter_username', 
            'avatar'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where are you based?'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            }),
            'github_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your GitHub username'
            }),
            'twitter_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Twitter username'
            })
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return avatar


# Contents from: .\projects\migrations\0001_initial.py
# Generated by Django 5.1.3 on 2024-11-17 21:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("github_link", models.URLField()),
                ("tags", models.CharField(blank=True, max_length=100)),
                ("claps", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="projects.comment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="projects.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Clap",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("clapped_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="claps_set",
                        to="projects.project",
                    ),
                ),
            ],
        ),
    ]


# Contents from: .\projects\migrations\0002_alter_comment_options_alter_project_options_and_more.py
# Generated by Django 5.1.3 on 2024-11-17 22:18

import django.core.validators
import projects.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ["created_at"]},
        ),
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="comment",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="project",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name="project",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="github_link",
            field=models.URLField(
                validators=[
                    django.core.validators.URLValidator(),
                    projects.models.validate_github_url,
                ]
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="tags",
            field=models.CharField(
                blank=True, help_text="Enter tags separated by commas", max_length=100
            ),
        ),
        migrations.AlterUniqueTogether(
            name="clap",
            unique_together={("project", "user")},
        ),
    ]


# Contents from: .\projects\migrations\0003_userprofile.py
# Generated by Django 5.1.3 on 2024-11-17 22:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0002_alter_comment_options_alter_project_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bio", models.TextField(blank=True, max_length=500)),
                ("location", models.CharField(blank=True, max_length=100)),
                ("github_username", models.CharField(blank=True, max_length=100)),
                ("linkedin_url", models.URLField(blank=True)),
                (
                    "avatar",
                    models.ImageField(blank=True, null=True, upload_to="avatars/"),
                ),
                ("website", models.URLField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]


# Contents from: .\projects\migrations\0004_notification.py
# Generated by Django 5.1.3 on 2024-11-17 22:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_userprofile"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("clap", "Clap"),
                            ("comment", "Comment"),
                            ("reply", "Reply"),
                            ("mention", "Mention"),
                            ("follow", "Follow"),
                        ],
                        max_length=20,
                    ),
                ),
                ("message", models.TextField()),
                ("is_read", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "comment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.comment",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]


# Contents from: .\projects\migrations\0005_remove_notification_comment_and_more.py
# Generated by Django 5.1.3 on 2024-11-17 23:06

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_notification"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="comment",
        ),
        migrations.AlterField(
            model_name="notification",
            name="notification_type",
            field=models.CharField(
                choices=[
                    ("clap", "Clap"),
                    ("comment", "Comment"),
                    ("reply", "Reply"),
                    ("mention", "Mention"),
                    ("follow", "Follow"),
                    ("rating", "Rating"),
                    ("bookmark", "Bookmark"),
                ],
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="ProjectAnalytics",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("view_count", models.PositiveIntegerField(default=0)),
                ("unique_visitors", models.PositiveIntegerField(default=0)),
                ("github_clicks", models.PositiveIntegerField(default=0)),
                ("avg_time_spent", models.DurationField(default=datetime.timedelta)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("direct_traffic", models.PositiveIntegerField(default=0)),
                ("social_traffic", models.PositiveIntegerField(default=0)),
                ("search_traffic", models.PositiveIntegerField(default=0)),
                ("referral_traffic", models.PositiveIntegerField(default=0)),
                ("desktop_visits", models.PositiveIntegerField(default=0)),
                ("mobile_visits", models.PositiveIntegerField(default=0)),
                ("tablet_visits", models.PositiveIntegerField(default=0)),
                ("chrome_visits", models.PositiveIntegerField(default=0)),
                ("firefox_visits", models.PositiveIntegerField(default=0)),
                ("safari_visits", models.PositiveIntegerField(default=0)),
                ("edge_visits", models.PositiveIntegerField(default=0)),
                ("other_browsers", models.PositiveIntegerField(default=0)),
                ("unique_visitors_weekly", models.PositiveIntegerField(default=0)),
                ("unique_visitors_monthly", models.PositiveIntegerField(default=0)),
                ("github_clicks_weekly", models.PositiveIntegerField(default=0)),
                ("github_clicks_monthly", models.PositiveIntegerField(default=0)),
                (
                    "project",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analytics",
                        to="projects.project",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Project analytics",
            },
        ),
        migrations.CreateModel(
            name="Bookmark",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "notes",
                    models.TextField(
                        blank=True, help_text="Add private notes about this project"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmarks",
                        to="projects.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmarks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "project")},
            },
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "score",
                    models.IntegerField(
                        choices=[
                            (1, "1 - Poor"),
                            (2, "2 - Fair"),
                            (3, "3 - Good"),
                            (4, "4 - Very Good"),
                            (5, "5 - Excellent"),
                        ]
                    ),
                ),
                ("review", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="projects.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("project", "user")},
            },
        ),
    ]


# Contents from: .\projects\migrations\0006_alter_bookmark_options_remove_bookmark_notes.py
# Generated by Django 5.1.3 on 2024-11-17 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0005_remove_notification_comment_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bookmark",
            options={"ordering": ["-created_at"]},
        ),
        migrations.RemoveField(
            model_name="bookmark",
            name="notes",
        ),
    ]


# Contents from: .\projects\migrations\0007_rename_clapped_at_clap_created_at_bookmark_notes_and_more.py
# Generated by Django 5.1.3 on 2024-11-18 04:04

import django.core.validators
import projects.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0006_alter_bookmark_options_remove_bookmark_notes"),
    ]

    operations = [
        migrations.RenameField(
            model_name="clap",
            old_name="clapped_at",
            new_name="created_at",
        ),
        migrations.AddField(
            model_name="bookmark",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="comment",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Upload an image (optional)",
                null=True,
                upload_to=projects.models.comment_image_upload_path,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="additional_files",
            field=models.FileField(
                blank=True,
                help_text="Upload additional files (PDF, DOC, TXT, ZIP - max 10MB)",
                null=True,
                upload_to=projects.models.project_file_upload_path,
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["pdf", "doc", "docx", "txt", "zip"]
                    )
                ],
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="featured_image",
            field=models.ImageField(
                blank=True,
                help_text="Upload a featured image for your project",
                null=True,
                upload_to=projects.models.project_image_upload_path,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="pdf_file",
            field=models.FileField(
                blank=True,
                help_text="Upload a PDF document (max 10MB)",
                null=True,
                upload_to=projects.models.project_file_upload_path,
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["pdf"]
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="avatar",
            field=models.ImageField(
                blank=True, null=True, upload_to=projects.models.avatar_upload_path
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="github_username",
            field=models.CharField(blank=True, max_length=39),
        ),
    ]


# Contents from: .\projects\migrations\0008_alter_notification_notification_type_and_more.py
# Generated by Django 5.1.3 on 2024-11-18 04:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0007_rename_clapped_at_clap_created_at_bookmark_notes_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="notification_type",
            field=models.CharField(
                choices=[
                    ("comment", "Comment"),
                    ("follow", "Follow"),
                    ("clap", "Clap"),
                    ("bookmark", "Bookmark"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]


# Contents from: .\projects\migrations\0009_follow.py
# Generated by Django 5.1.3 on 2024-11-18 04:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0008_alter_notification_notification_type_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Follow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "follower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "following",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("follower", "following")},
            },
        ),
    ]


# Contents from: .\projects\migrations\__init__.py


# Contents from: .\projects\models.py
# projects/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from datetime import timedelta
import os
from django.db.models.signals import post_save
from django.dispatch import receiver

# File Upload Path Functions
def validate_github_url(value):
    if not value.startswith(('https://github.com/', 'http://github.com/')):
        raise ValidationError('URL must be a GitHub repository')

def project_file_upload_path(instance, filename):
    """Generate upload path for project files"""
    return f'uploads/user_{instance.author.id}/project_{instance.pk}/{filename}'

def project_image_upload_path(instance, filename):
    """Generate upload path for project images"""
    return f'images/projects/user_{instance.author.id}/{filename}'

def avatar_upload_path(instance, filename):
    """Generate upload path for user avatars"""
    return f'avatars/user_{instance.user.id}/{filename}'

def comment_image_upload_path(instance, filename):
    """Generate upload path for comment images"""
    return f'images/comments/user_{instance.user.id}/{filename}'

# Models
class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    github_link = models.URLField(validators=[URLValidator(), validate_github_url])
    tags = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Enter tags separated by commas"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    claps = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # File fields
    pdf_file = models.FileField(
        upload_to=project_file_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        null=True,
        blank=True,
        help_text="Upload a PDF document (max 10MB)"
    )
    
    featured_image = models.ImageField(
        upload_to=project_image_upload_path,
        null=True,
        blank=True,
        help_text="Upload a featured image for your project"
    )
    
    additional_files = models.FileField(
        upload_to=project_file_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'zip']
            )
        ],
        null=True,
        blank=True,
        help_text="Upload additional files (PDF, DOC, TXT, ZIP - max 10MB)"
    )
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Create upload directory if it doesn't exist
        if not self.pk:  # Only for new instances
            super().save(*args, **kwargs)
            upload_dir = os.path.dirname(project_file_upload_path(self, ''))
            os.makedirs(os.path.join('media', upload_dir), exist_ok=True)
        else:
            super().save(*args, **kwargs)
    
    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    @property
    def comment_count(self):
        return self.comments.count()
        
    def user_has_clapped(self, user):
        return self.claps_set.filter(user=user).exists()
    
    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if not ratings:
            return None
        return sum(r.score for r in ratings) / len(ratings)

    def clean(self):
        super().clean()
        # Validate file sizes
        if self.pdf_file and self.pdf_file.size > 10 * 1024 * 1024:  # 10MB
            raise ValidationError({'pdf_file': 'PDF file must be smaller than 10MB'})
        if self.additional_files and self.additional_files.size > 10 * 1024 * 1024:
            raise ValidationError({'additional_files': 'File must be smaller than 10MB'})
        if self.featured_image and self.featured_image.size > 5 * 1024 * 1024:  # 5MB
            raise ValidationError({'featured_image': 'Image must be smaller than 5MB'})

class Comment(models.Model):
    project = models.ForeignKey(
        Project, 
        related_name='comments', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    image = models.ImageField(
        upload_to=comment_image_upload_path,
        null=True,
        blank=True,
        help_text="Upload an image (optional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.project.title}'

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    github_username = models.CharField(max_length=39, blank=True)
    linkedin_url = models.URLField(blank=True)
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    @property
    def project_count(self):
        return self.user.project_set.count()
    
    @property
    def total_claps_received(self):
        return sum(project.claps for project in self.user.project_set.all())

class Clap(models.Model):
    project = models.ForeignKey(
        Project, 
        related_name='claps_set', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('project', 'user')
    
    def __str__(self):
        return f'{self.user.username} clapped for {self.project.title}'

class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent')
    )
    
    project = models.ForeignKey(
        Project, 
        related_name='ratings', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('project', 'user')
        
    def __str__(self):
        return f"{self.user.username}'s {self.score}-star rating on {self.project.title}"

class Bookmark(models.Model):
    user = models.ForeignKey(
        User, 
        related_name='bookmarks', 
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project, 
        related_name='bookmarks', 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('user', 'project')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.project.title}"

class ProjectAnalytics(models.Model):
    project = models.OneToOneField(
        Project, 
        on_delete=models.CASCADE, 
        related_name='analytics'
    )
    view_count = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    github_clicks = models.PositiveIntegerField(default=0)
    avg_time_spent = models.DurationField(default=timedelta)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Traffic sources
    direct_traffic = models.PositiveIntegerField(default=0)
    social_traffic = models.PositiveIntegerField(default=0)
    search_traffic = models.PositiveIntegerField(default=0)
    referral_traffic = models.PositiveIntegerField(default=0)
    
    # Device stats
    desktop_visits = models.PositiveIntegerField(default=0)
    mobile_visits = models.PositiveIntegerField(default=0)
    tablet_visits = models.PositiveIntegerField(default=0)
    
    # Browser stats
    chrome_visits = models.PositiveIntegerField(default=0)
    firefox_visits = models.PositiveIntegerField(default=0)
    safari_visits = models.PositiveIntegerField(default=0)
    edge_visits = models.PositiveIntegerField(default=0)
    other_browsers = models.PositiveIntegerField(default=0)
    
    # Weekly and monthly stats
    unique_visitors_weekly = models.PositiveIntegerField(default=0)
    unique_visitors_monthly = models.PositiveIntegerField(default=0)
    github_clicks_weekly = models.PositiveIntegerField(default=0)
    github_clicks_monthly = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Project analytics"
        
    def __str__(self):
        return f"Analytics for {self.project.title}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('clap', 'Clap'),
        ('bookmark', 'Bookmark'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Notification for {self.recipient.username}'

    @classmethod
    def create(cls, recipient, sender, notification_type, project=None, message=None):
        if not message:
            message = cls.get_default_message(notification_type, sender, project)
        return cls.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            project=project,
            message=message
        )

    @staticmethod
    def get_default_message(notification_type, sender, project=None):
        username = sender.username
        if project:
            project_title = project.title
            if notification_type == 'clap':
                return f"{username} clapped for your project '{project_title}'"
            elif notification_type == 'comment':
                return f"{username} commented on your project '{project_title}'"
            elif notification_type == 'rating':
                return f"{username} rated your project '{project_title}'"
            elif notification_type == 'bookmark':
                return f"{username} bookmarked your project '{project_title}'"
        elif notification_type == 'follow':
            return f"{username} started following you"
        return "You have a new notification"

class Follow(models.Model):
    follower = models.ForeignKey(
        User, 
        related_name='following',  # User.following.all() gets all users this user follows
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, 
        related_name='followers',  # User.followers.all() gets all users following this user
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    twitter_username = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Notification settings
    email_on_comment = models.BooleanField(default=True)
    email_on_follow = models.BooleanField(default=True)
    email_on_clap = models.BooleanField(default=False)
    email_on_bookmark = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

# Contents from: .\projects\serializers.py
# projects/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Project,
    Comment,
    UserProfile,
    Rating,
    Bookmark,
    ProjectAnalytics,
    Notification
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'bio', 'location', 'website',
            'github_username', 'linkedin_url', 'avatar'
        ]

class ProjectSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tag_list = serializers.ListField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description',
            'github_link', 'tags', 'author',
            'claps', 'created_at', 'updated_at',
            'pdf_file', 'featured_image',
            'additional_files', 'tag_list',
            'comment_count', 'average_rating'
        ]
        read_only_fields = ['slug', 'claps']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'project', 'user', 'parent',
            'content', 'image', 'created_at',
            'updated_at', 'replies'
        ]
        read_only_fields = ['user']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = [
            'id', 'project', 'user', 'score',
            'review', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user']

class BookmarkSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'project', 'created_at', 'notes']
        read_only_fields = ['user']

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'sender', 'project',
            'notification_type', 'message', 'is_read',
            'created_at'
        ]
        read_only_fields = ['recipient', 'sender', 'project']

class ProjectAnalyticsSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    device_distribution = serializers.SerializerMethodField()
    browser_distribution = serializers.SerializerMethodField()
    traffic_sources = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectAnalytics
        fields = [
            'project', 'view_count', 'unique_visitors',
            'github_clicks', 'avg_time_spent',
            'direct_traffic', 'social_traffic',
            'search_traffic', 'referral_traffic',
            'desktop_visits', 'mobile_visits',
            'tablet_visits', 'chrome_visits',
            'firefox_visits', 'safari_visits',
            'edge_visits', 'other_browsers',
            'unique_visitors_weekly', 'unique_visitors_monthly',
            'github_clicks_weekly', 'github_clicks_monthly',
            'device_distribution', 'browser_distribution',
            'traffic_sources', 'last_updated'
        ]
        read_only_fields = ['project']
    
    def get_device_distribution(self, obj):
        total = obj.desktop_visits + obj.mobile_visits + obj.tablet_visits
        if total == 0:
            return {
                'desktop': 0,
                'mobile': 0,
                'tablet': 0
            }
        
        return {
            'desktop': round((obj.desktop_visits / total) * 100, 1),
            'mobile': round((obj.mobile_visits / total) * 100, 1),
            'tablet': round((obj.tablet_visits / total) * 100, 1)
        }
    
    def get_browser_distribution(self, obj):
        total = (
            obj.chrome_visits + obj.firefox_visits +
            obj.safari_visits + obj.edge_visits + obj.other_browsers
        )
        
        if total == 0:
            return {
                'chrome': 0,
                'firefox': 0,
                'safari': 0,
                'edge': 0,
                'other': 0
            }
        
        return {
            'chrome': round((obj.chrome_visits / total) * 100, 1),
            'firefox': round((obj.firefox_visits / total) * 100, 1),
            'safari': round((obj.safari_visits / total) * 100, 1),
            'edge': round((obj.edge_visits / total) * 100, 1),
            'other': round((obj.other_browsers / total) * 100, 1)
        }
    
    def get_traffic_sources(self, obj):
        total = (
            obj.direct_traffic + obj.social_traffic +
            obj.search_traffic + obj.referral_traffic
        )
        
        if total == 0:
            return {
                'direct': 0,
                'social': 0,
                'search': 0,
                'referral': 0
            }
        
        return {
            'direct': round((obj.direct_traffic / total) * 100, 1),
            'social': round((obj.social_traffic / total) * 100, 1),
            'search': round((obj.search_traffic / total) * 100, 1),
            'referral': round((obj.referral_traffic / total) * 100, 1)
        }

class ProjectAnalyticsSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for analytics summary"""
    class Meta:
        model = ProjectAnalytics
        fields = ['view_count', 'unique_visitors', 'github_clicks']

# Contents from: .\projects\templatetags\search_tags.py
# projects/templatetags/search_tags.py

from django import template
from django.utils.html import mark_safe
from django.utils.html import escape
import re

register = template.Library()

@register.filter(name='highlight')
def highlight_search_term(text, search_term):
    """Highlight search terms in text while preserving HTML safety"""
    if not search_term or not text:
        return text
    
    text = str(text)
    search_term = str(search_term)
    
    # Escape HTML in the text
    text = escape(text)
    
    # Create a pattern that matches whole words
    pattern = r'({})'.format(re.escape(search_term))
    
    # Replace matches with highlighted version
    highlighted = re.sub(
        pattern,
        r'<mark class="highlight">\1</mark>',
        text,
        flags=re.IGNORECASE
    )
    
    return mark_safe(highlighted)

@register.filter(name='querystring_without')
def querystring_without(query_dict, key):
    """Remove a key from querystring while preserving other parameters"""
    query_dict = query_dict.copy()
    query_dict.pop(key, None)
    return query_dict.urlencode()

@register.simple_tag
def url_with_querystring(request, **kwargs):
    """Build URL with updated querystring parameters"""
    query_dict = request.GET.copy()
    for key, value in kwargs.items():
        query_dict[key] = value
    return '?{}'.format(query_dict.urlencode())

# Contents from: .\projects\tests.py
from django.test import TestCase

# Create your tests here.


# Contents from: .\projects\urls.py
# projects/urls.py

from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # Project Management
    path('', views.project_list, name='project_list'),
    path('submit/', views.submit_project, name='submit_project'),
    path('search/', views.search_projects, name='search_projects'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    
    # Project Detail & Actions
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('project/<int:pk>/rate/', views.rate_project, name='rate_project'),
    path('project/<int:pk>/bookmark/', views.bookmark_project, name='bookmark_project'),
    path('project/<int:pk>/clap/', views.clap_project, name='clap_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    
    # Analytics
    path('project/<int:pk>/analytics/', views.ProjectAnalyticsView.as_view(), name='project_analytics'),
    path('project/<int:pk>/analytics/data/', views.analytics_data, name='analytics_data'),
    path('project/<int:pk>/analytics/export/csv/', views.export_analytics_csv, name='export_analytics_csv'),
    path('project/<int:pk>/analytics/export/pdf/', views.export_analytics_pdf, name='export_analytics_pdf'),
    
    # User Profiles - Note the reordered URLs
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Moved before username pattern
    path('profile/settings/', views.profile_settings, name='profile_settings'),  # Added settings
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/projects/', views.user_projects, name='user_projects'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', 
         views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', 
         views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Comments
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    
    # API Endpoints
    path('api/projects/', views.ProjectListAPI.as_view(), name='api_project_list'),
    path('api/projects/<int:pk>/', views.ProjectDetailAPI.as_view(), name='api_project_detail'),
    path('api/projects/<int:pk>/analytics/', views.ProjectAnalyticsAPI.as_view(), name='api_project_analytics'),
]

# Contents from: .\projects\utils\__init__.py
# This file can be empty

# Contents from: .\projects\utils\emails.py
# projects/utils/emails.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_notification_email(notification):
    """Send email for a new notification"""
    subject = f'New notification from {settings.SITE_NAME}'
    context = {
        'notification': notification,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/notification.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [notification.recipient.email],
        html_message=html_message,
        fail_silently=True
    )

def send_welcome_email(user):
    """Send welcome email to new users"""
    subject = f'Welcome to {settings.SITE_NAME}'
    context = {
        'user': user,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/welcome.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True
    )

def send_comment_notification(comment):
    """Send email notification for new comments"""
    subject = f'New comment on your project - {settings.SITE_NAME}'
    context = {
        'comment': comment,
        'project': comment.project,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/project_comment.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [comment.project.author.email],
        html_message=html_message,
        fail_silently=True
    )

def send_clap_notification(clap):
    """Send email notification for new claps"""
    subject = f'Someone appreciated your project - {settings.SITE_NAME}'
    context = {
        'clap': clap,
        'project': clap.project,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/project_clap.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [clap.project.author.email],
        html_message=html_message,
        fail_silently=True
    )

# Contents from: .\projects\utils\pdf.py
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

def generate_analytics_pdf(project, analytics_data):
    """Generate a PDF report for project analytics"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph(f"Analytics Report: {project.title}", title_style))
    story.append(Spacer(1, 12))

    # Overview Section
    story.append(Paragraph("Overview", styles['Heading2']))
    overview_data = [
        ["Total Views", str(analytics_data.get('view_count', 0))],
        ["Unique Visitors", str(analytics_data.get('unique_visitors', 0))],
        ["GitHub Clicks", str(analytics_data.get('github_clicks', 0))],
    ]
    overview_table = Table(overview_data, colWidths=[2*inch, 2*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(overview_table)
    story.append(Spacer(1, 20))

    # Traffic Sources
    story.append(Paragraph("Traffic Sources", styles['Heading2']))
    traffic_data = [
        ["Direct", f"{analytics_data.get('direct_traffic', 0)}%"],
        ["Social", f"{analytics_data.get('social_traffic', 0)}%"],
        ["Search", f"{analytics_data.get('search_traffic', 0)}%"],
        ["Referral", f"{analytics_data.get('referral_traffic', 0)}%"],
    ]
    traffic_table = Table(traffic_data, colWidths=[2*inch, 2*inch])
    traffic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(traffic_table)
    story.append(Spacer(1, 20))

    # Device Distribution
    story.append(Paragraph("Device Distribution", styles['Heading2']))
    device_data = [
        ["Desktop", f"{analytics_data.get('desktop_visits', 0)}%"],
        ["Mobile", f"{analytics_data.get('mobile_visits', 0)}%"],
        ["Tablet", f"{analytics_data.get('tablet_visits', 0)}%"],
    ]
    device_table = Table(device_data, colWidths=[2*inch, 2*inch])
    device_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(device_table)

    # Build PDF
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# Contents from: .\projects\views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q, Avg, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.core.cache import cache
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.core.files.storage import default_storage
import csv
import json
import os
import pytz
from datetime import datetime, timedelta
from io import StringIO
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer, ProjectAnalyticsSerializer, ProjectAnalyticsSummarySerializer

from .models import (
    Project, Comment, Clap, UserProfile, Rating, 
    Bookmark, ProjectAnalytics, Notification, Follow
)
from .forms import (
    ProjectForm, CommentForm, ProjectSearchForm, UserProfileForm,
    RatingForm, BookmarkForm, AdvancedSearchForm, ProfileForm, NotificationSettingsForm
)
from .filters.project_filters import ProjectFilter
from django.contrib.auth.forms import UserCreationForm
from .utils.pdf import generate_analytics_pdf

class ProjectAnalyticsView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_analytics.html'
    context_object_name = 'project'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analytics = self.object.analytics
        now = timezone.now()
        
        # Calculate date ranges
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # Get weekly and monthly stats
        weekly_stats = {
            'views': analytics.get_views_count(since=week_ago),
            'unique_visitors': analytics.get_unique_visitors_count(since=week_ago),
            'github_clicks': analytics.get_github_clicks_count(since=week_ago),
            'comments': self.object.comments.filter(created_at__gte=week_ago).count(),
            'claps': self.object.claps_set.filter(created_at__gte=week_ago).count(),
            'ratings': self.object.ratings.filter(created_at__gte=week_ago).count()
        }
        
        monthly_stats = {
            'views': analytics.get_views_count(since=month_ago),
            'unique_visitors': analytics.get_unique_visitors_count(since=month_ago),
            'github_clicks': analytics.get_github_clicks_count(since=month_ago),
            'comments': self.object.comments.filter(created_at__gte=month_ago).count(),
            'claps': self.object.claps_set.filter(created_at__gte=month_ago).count(),
            'ratings': self.object.ratings.filter(created_at__gte=month_ago).count()
        }
        
        # Calculate trends
        def calculate_trend(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            return round(((current - previous) / previous) * 100, 1)

        trends = {
            'views': calculate_trend(
                weekly_stats['views'], 
                analytics.get_views_count(since=week_ago - timedelta(days=7), until=week_ago)
            ),
            'visitors': calculate_trend(
                weekly_stats['unique_visitors'],
                analytics.get_unique_visitors_count(since=week_ago - timedelta(days=7), until=week_ago)
            ),
            'github': calculate_trend(
                weekly_stats['github_clicks'],
                analytics.get_github_clicks_count(since=week_ago - timedelta(days=7), until=week_ago)
            )
        }
        
        # Get traffic sources breakdown
        total_traffic = (
            analytics.direct_traffic + 
            analytics.social_traffic + 
            analytics.search_traffic + 
            analytics.referral_traffic
        )
        
        traffic_sources = {
            'direct': {
                'count': analytics.direct_traffic,
                'percentage': round((analytics.direct_traffic / total_traffic * 100), 1) if total_traffic > 0 else 0
            },
            'social': {
                'count': analytics.social_traffic,
                'percentage': round((analytics.social_traffic / total_traffic * 100), 1) if total_traffic > 0 else 0
            },
            'search': {
                'count': analytics.search_traffic,
                'percentage': round((analytics.search_traffic / total_traffic * 100), 1) if total_traffic > 0 else 0
            },
            'referral': {
                'count': analytics.referral_traffic,
                'percentage': round((analytics.referral_traffic / total_traffic * 100), 1) if total_traffic > 0 else 0
            }
        }
        
        # Device and browser stats
        total_visits = (
            analytics.desktop_visits + 
            analytics.mobile_visits + 
            analytics.tablet_visits
        )
        
        devices = {
            'desktop': {
                'count': analytics.desktop_visits,
                'percentage': round((analytics.desktop_visits / total_visits * 100), 1) if total_visits > 0 else 0
            },
            'mobile': {
                'count': analytics.mobile_visits,
                'percentage': round((analytics.mobile_visits / total_visits * 100), 1) if total_visits > 0 else 0
            },
            'tablet': {
                'count': analytics.tablet_visits,
                'percentage': round((analytics.tablet_visits / total_visits * 100), 1) if total_visits > 0 else 0
            }
        }
        
        total_browser_visits = (
            analytics.chrome_visits +
            analytics.firefox_visits +
            analytics.safari_visits +
            analytics.edge_visits +
            analytics.other_browsers
        )
        
        browsers = [
            {
                'name': 'Chrome',
                'count': analytics.chrome_visits,
                'percentage': round((analytics.chrome_visits / total_browser_visits * 100), 1) if total_browser_visits > 0 else 0,
                'color': '#4285F4',
                'icon': 'browser-chrome'
            },
            {
                'name': 'Firefox',
                'count': analytics.firefox_visits,
                'percentage': round((analytics.firefox_visits / total_browser_visits * 100), 1) if total_browser_visits > 0 else 0,
                'color': '#FF7139',
                'icon': 'browser-firefox'
            },
            {
                'name': 'Safari',
                'count': analytics.safari_visits,
                'percentage': round((analytics.safari_visits / total_browser_visits * 100), 1) if total_browser_visits > 0 else 0,
                'color': '#000000',
                'icon': 'browser-safari'
            },
            {
                'name': 'Edge',
                'count': analytics.edge_visits,
                'percentage': round((analytics.edge_visits / total_browser_visits * 100), 1) if total_browser_visits > 0 else 0,
                'color': '#0078D7',
                'icon': 'browser-edge'
            },
            {
                'name': 'Other',
                'count': analytics.other_browsers,
                'percentage': round((analytics.other_browsers / total_browser_visits * 100), 1) if total_browser_visits > 0 else 0,
                'color': '#6B7280',
                'icon': 'browser'
            }
        ]
        
        # Get time series data for charts
        time_series_data = analytics.get_time_series_data(days=30)
        
        context.update({
            'analytics': analytics,
            'weekly_stats': weekly_stats,
            'monthly_stats': monthly_stats,
            'trends': trends,
            'traffic_sources': traffic_sources,
            'devices': devices,
            'browsers': browsers,
            'time_series_data': time_series_data,
            'now': now
        })
        
        return context

def analytics_data(request, pk):
    """API endpoint for fetching analytics data"""
    project = get_object_or_404(Project, pk=pk)
    if project.author != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    analytics = project.analytics
    time_range = request.GET.get('range', 'week')
    
    if time_range == 'week':
        days = 7
    elif time_range == 'month':
        days = 30
    else:
        days = 365
    
    data = analytics.get_time_series_data(days=days)
    
    return JsonResponse(data)

def export_analytics_csv(request, pk):
    """Export analytics data as CSV"""
    project = get_object_or_404(Project, pk=pk)
    if project.author != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    analytics = project.analytics
    
    # Create CSV data
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Date', 'Views', 'Unique Visitors', 'GitHub Clicks',
        'Average Time (minutes)', 'Comments', 'Claps'
    ])
    
    # Get daily data for the last 30 days
    data = analytics.get_time_series_data(days=30)
    for entry in data['daily_data']:
        writer.writerow([
            entry['date'],
            entry['views'],
            entry['visitors'],
            entry['github_clicks'],
            round(entry['avg_time_spent'] / 60, 2),
            entry['comments'],
            entry['claps']
        ])
    
    # Create the HTTP response with CSV data
    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{project.slug}-analytics.csv"'
    
    return response

def export_analytics_pdf(request, pk):
    """Export analytics data as PDF"""
    if not request.method == 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    project = get_object_or_404(Project, pk=pk)
    if project.author != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    data = json.loads(request.body)
    chart_images = data.get('charts', {})
    date_range = data.get('dateRange', 'week')
    
    # Generate PDF using the utility function
    pdf_file = generate_analytics_pdf(project, chart_images, date_range)
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{project.slug}-analytics.pdf"'
    
    return response

def get_popular_tags():
    """Helper function to get popular tags"""
    return (Project.objects
            .values('tags')
            .annotate(count=Count('id'))
            .order_by('-count')
            .exclude(tags='')[:10])

def get_client_info(request):
    """Get basic client information without user-agents package"""
    info = {
        'is_mobile': request.META.get('HTTP_USER_AGENT', '').lower().find('mobile') > -1,
        'browser': 'other',
        'ip': request.META.get('REMOTE_ADDR'),
        'referrer': request.META.get('HTTP_REFERER', ''),
    }
    
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    if 'chrome' in user_agent:
        info['browser'] = 'chrome'
    elif 'firefox' in user_agent:
        info['browser'] = 'firefox'
    elif 'safari' in user_agent:
        info['browser'] = 'safari'
    elif 'edge' in user_agent:
        info['browser'] = 'edge'
    
    return info

def update_analytics(request, project):
    """Update project analytics"""
    analytics, created = ProjectAnalytics.objects.get_or_create(project=project)
    client_info = get_client_info(request)
    
    # Update view count
    analytics.view_count += 1
    
    # Update device stats
    if client_info['is_mobile']:
        analytics.mobile_visits += 1
    else:
        analytics.desktop_visits += 1
    
    # Update browser stats
    if client_info['browser'] == 'chrome':
        analytics.chrome_visits += 1
    elif client_info['browser'] == 'firefox':
        analytics.firefox_visits += 1
    elif client_info['browser'] == 'safari':
        analytics.safari_visits += 1
    elif client_info['browser'] == 'edge':
        analytics.edge_visits += 1
    else:
        analytics.other_browsers += 1
    
    # Update traffic sources
    referrer = client_info['referrer']
    if not referrer:
        analytics.direct_traffic += 1
    elif 'google' in referrer or 'bing' in referrer:
        analytics.search_traffic += 1
    elif 'facebook' in referrer or 'twitter' in referrer or 'linkedin' in referrer:
        analytics.social_traffic += 1
    else:
        analytics.referral_traffic += 1
    
    # Update unique visitors
    visitor_key = f"visitor_{client_info['ip']}_{project.id}"
    if not cache.get(visitor_key):
        analytics.unique_visitors += 1
        cache.set(visitor_key, True, timeout=86400)  # 24 hours
        
        # Update weekly and monthly unique visitors
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        if not cache.get(f"{visitor_key}_weekly"):
            analytics.unique_visitors_weekly += 1
            cache.set(f"{visitor_key}_weekly", True, timeout=604800)  # 7 days
            
        if not cache.get(f"{visitor_key}_monthly"):
            analytics.unique_visitors_monthly += 1
            cache.set(f"{visitor_key}_monthly", True, timeout=2592000)  # 30 days
    
    analytics.save()

def project_list(request):
    """List and search projects"""
    search_form = ProjectSearchForm(request.GET)
    projects = Project.objects.all()
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        tags = search_form.cleaned_data.get('tags')
        sort = search_form.cleaned_data.get('sort')
        
        if query:
            projects = projects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(author__username__icontains=query) |
                Q(tags__icontains=query)
            )
        
        if tags:
            for tag in tags:
                projects = projects.filter(tags__icontains=tag)
        
        if sort:
            projects = projects.order_by(sort)
        else:
            projects = projects.order_by('-created_at')
    else:
        projects = projects.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(projects, 12)
    page = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    # Get popular tags
    popular_tags = (Project.objects
        .values_list('tags', flat=True)
        .exclude(tags='')
        .annotate(count=Count('id'))
        .order_by('-count')[:10])
    
    context = {
        'page_obj': page_obj,
        'popular_tags': popular_tags,
        'search_form': search_form,
    }
    return render(request, 'projects/project_list.html', context)

@login_required
def submit_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            
            # Handle featured image
            if 'featured_image' in request.FILES:
                project.featured_image = form.cleaned_data['featured_image']
            
            project.save()
            
            # Create project directory
            project_dir = f'uploads/user_{request.user.id}/project_{project.id}'
            os.makedirs(os.path.join(settings.MEDIA_ROOT, project_dir), exist_ok=True)
            
            messages.success(request, 'Project submitted successfully!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    return render(request, 'projects/submit_project.html', {'form': form})



def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    comments = project.comments.filter(parent=None).select_related('user').prefetch_related('replies')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
            
            # Create notification for project author
            if project.author != request.user:
                Notification.objects.create(
                    recipient=project.author,
                    sender=request.user,
                    project=project,
                    notification_type='comment',
                    message=f"{request.user.username} commented on your project"
                )
            
            messages.success(request, 'Comment added successfully!')
            return redirect('project_detail', pk=pk)
    else:
        form = CommentForm()
    
    context = {
        'project': project,
        'comments': comments,
        'form': form,
    }
    return render(request, 'projects/project_detail.html', context)



@login_required
def rate_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        form = RatingForm(request.POST)
        
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                project=project,
                user=request.user,
                defaults={
                    'score': form.cleaned_data['score'],
                    'review': form.cleaned_data['review']
                }
            )
            
            # Update project rating cache
            avg_rating = project.ratings.aggregate(Avg('score'))['score__avg']
            cache.set(f'project_rating_{project.id}', avg_rating, timeout=3600)
            
            messages.success(request, 'Thank you for your rating!')
            return JsonResponse({
                'status': 'success',
                'rating': avg_rating,
                'total_ratings': project.ratings.count()
            })
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def toggle_bookmark(request, pk):
    project = get_object_or_404(Project, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(
        project=project,
        user=request.user,
        defaults={'notes': ''}
    )
    
    if not created:
        bookmark.delete()
        return JsonResponse({'status': 'removed'})
    
    return JsonResponse({'status': 'added'})

@login_required
def update_bookmark_notes(request, pk):
    bookmark = get_object_or_404(Bookmark, project_id=pk, user=request.user)
    
    if request.method == 'POST':
        form = BookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('project')
    return render(request, 'projects/bookmarks.html', {'bookmarks': bookmarks})



@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'projects/edit_profile.html', {'form': form})

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    projects = Project.objects.filter(author=profile_user).order_by('-created_at')
    
    # Get follow status
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()
    
    # Get counts
    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    
    context = {
        'profile_user': profile_user,
        'projects': projects,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'projects/user_profile.html', context)

def user_projects(request, username):
    user = get_object_or_404(User, username=username)
    projects = user.project_set.all().order_by('-created_at')
    
    # Filter by tag if provided
    tag = request.GET.get('tag')
    if tag:
        projects = projects.filter(tags__icontains=tag)
    
    paginator = Paginator(projects, 10)
    page = request.GET.get('page')
    projects_page = paginator.get_page(page)
    
    context = {
        'user_profile': user,
        'projects': projects_page,
        'selected_tag': tag,
    }
    return render(request, 'projects/user_projects.html', context)

@login_required
def notifications(request):
    notifications_list = request.user.notifications.all().order_by('-created_at')
    return render(request, 'projects/notifications.html', {
        'notifications': notifications_list
    })

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user != user_to_follow:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if created:
            # Create notification for the followed user
            Notification.objects.create(
                recipient=user_to_follow,
                sender=request.user,
                notification_type='follow',
                message=f'{request.user.username} started following you'
            )
    
    return redirect('projects:user_profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    
    Follow.objects.filter(
        follower=request.user,
        following=user_to_unfollow
    ).delete()
    
    return redirect('projects:user_profile', username=username)

def search_projects(request):
    """Advanced search view"""
    form = AdvancedSearchForm(request.GET)
    projects = Project.objects.all()
    
    if form.is_valid():
        # Apply filters using ProjectFilter
        project_filter = ProjectFilter(request.GET, queryset=projects)
        projects = project_filter.qs
        
        # Apply sorting
        sort_by = form.cleaned_data.get('sort_by')
        if sort_by:
            if sort_by == '-rating_avg':
                # Annotate with average rating
                projects = projects.annotate(
                    rating_avg=Avg('ratings__score')
                ).order_by('-rating_avg')
            elif sort_by == '-comment_count':
                # Annotate with comment count
                projects = projects.annotate(
                    comment_count=Count('comments')
                ).order_by('-comment_count')
            else:
                projects = projects.order_by(sort_by)
    
    # Annotate with additional metrics for display
    projects = projects.annotate(
        comment_count=Count('comments'),
        rating_avg=Avg('ratings__score')
    )
    
    # Pagination
    paginator = Paginator(projects, settings.MAX_PROJECTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    
    context = {
        'form': form,
        'projects': projects,
        'popular_tags': get_popular_tags(),
        'total_results': paginator.count,
    }
    
    if request.headers.get('HX-Request'):
        # Return partial template for HTMX requests
        return render(request, 'projects/includes/project_list_results.html', context)
    
    return render(request, 'projects/search.html', context)

@login_required
def bookmark_project(request, pk):
    """Add or remove a project bookmark"""
    project = get_object_or_404(Project, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        project=project
    )
    
    if not created:
        # If bookmark already existed, remove it
        bookmark.delete()
        messages.success(request, 'Bookmark removed.')
        return JsonResponse({
            'status': 'success',
            'action': 'removed',
            'message': 'Project removed from bookmarks'
        })
    
    # Create notification for project author
    if project.author != request.user:
        Notification.create_notification(
            recipient=project.author,
            sender=request.user,
            notification_type='bookmark',
            project=project
        )
    
    messages.success(request, 'Project bookmarked successfully.')
    return JsonResponse({
        'status': 'success',
        'action': 'added',
        'message': 'Project added to bookmarks'
    })

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

def get_monthly_contributions():
    """Calculate monthly contributions for all users"""
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    return User.objects.annotate(
        projects_count=Count(
            'project',
            filter=models.Q(project__created_at__gte=start_of_month)
        ),
        claps_received=Sum(
            'project__claps',
            filter=models.Q(project__created_at__gte=start_of_month)
        ),
        total_contributions=models.F('projects_count') + models.F('claps_received')
    ).filter(
        models.Q(projects_count__gt=0) | models.Q(claps_received__gt=0)
    ).order_by('-total_contributions')[:10]

def leaderboard_view(request):
    """View for the leaderboard page"""
    contributions = get_monthly_contributions()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON for React component
        data = [{
            'rank': idx + 1,
            'user': user.username,
            'contributions': user.total_contributions,
            'projects': user.projects_count,
            'claps': user.claps_received or 0,
            'change': 0  # Calculate change from previous position
        } for idx, user in enumerate(contributions)]
        return JsonResponse({'leaderboard': data})
    
    return render(request, 'projects/leaderboard.html', {
        'contributions': contributions
    })


#####
# views.py (add these methods)



@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('projects:project_list')
    return render(request, 'projects/delete_project.html', {'project': project})



@login_required
def clap_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        clap, created = Clap.objects.get_or_create(user=request.user, project=project)
        if created:
            project.claps += 1
            project.save()
            return JsonResponse({'status': 'success', 'claps': project.claps})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('projects:project_detail', pk=comment.project.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'projects/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user and comment.project.author != request.user:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    project_pk = comment.project.pk
    comment.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('projects:project_detail', pk=project_pk)

@login_required
def mark_all_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

# API Views
class ProjectListAPI(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class ProjectDetailAPI(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class ProjectAnalyticsAPI(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        project = super().get_object()
        if project.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied
        return project.analytics

@login_required
def profile_settings(request):
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST)
        if form.is_valid():
            # Update notification settings
            user_profile.email_on_comment = form.cleaned_data['email_on_comment']
            user_profile.email_on_follow = form.cleaned_data['email_on_follow']
            user_profile.email_on_clap = form.cleaned_data['email_on_clap']
            user_profile.email_on_bookmark = form.cleaned_data['email_on_bookmark']
            user_profile.save()
            
            messages.success(request, 'Settings updated successfully!')
            return redirect('projects:profile_settings')
    else:
        # Initialize form with current settings
        form = NotificationSettingsForm(initial={
            'email_on_comment': user_profile.email_on_comment,
            'email_on_follow': user_profile.email_on_follow,
            'email_on_clap': user_profile.email_on_clap,
            'email_on_bookmark': user_profile.email_on_bookmark,
        })

    return render(request, 'projects/profile_settings.html', {
        'form': form,
        'active_tab': 'settings'
    })