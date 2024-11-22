# Combined Python and HTML files
# Generated from directory: C:\Users\isult\OneDrive\Documents\khcc_psut_ai_lab\khcc_psut_ai_lab\templates
# Total files found: 61



# Contents from: .\account\email_confirm.html
{% extends "base.html" %}
{% load i18n %}
{% load account %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-body p-4">
                    <h2 class="card-title text-center mb-4">{% trans "Confirm Email Address" %}</h2>
                    
                    {% if confirmation %}
                        {% user_display confirmation.email_address.user as user_display %}
                        
                        <p class="text-center mb-4">
                            {% blocktrans with confirmation.email_address.email as email %}
                            Please confirm that <strong>{{ email }}</strong> is an email address for user <strong>{{ user_display }}</strong>.
                            {% endblocktrans %}
                        </p>

                        <form method="post" action="{% url 'account_confirm_email' confirmation.key %}">
                            {% csrf_token %}
                            <div class="d-grid gap-2">
                                <button class="btn btn-primary" type="submit">
                                    {% trans 'Confirm' %}
                                </button>
                            </div>
                        </form>
                    
                    {% else %}
                        {% url 'account_email' as email_url %}
                        
                        <div class="text-center">
                            <div class="alert alert-warning" role="alert">
                                {% blocktrans %}
                                This email confirmation link has expired or is invalid. 
                                Please <a href="{{ email_url }}" class="alert-link">request a new confirmation email</a>.
                                {% endblocktrans %}
                            </div>
                            
                            <div class="mt-4">
                                <a href="{% url 'account_login' %}" class="btn btn-outline-primary">
                                    {% trans "Return to Login" %}
                                </a>
                            </div>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\account\login.html
{% extends "base.html" %}
{% load i18n %}
{% load account socialaccount %}
{% load crispy_forms_tags %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-body p-4">
                    <h2 class="card-title text-center mb-4">{% trans "Sign In" %}</h2>
                    
                    <form class="login" method="POST" action="{% url 'account_login' %}">
                        {% csrf_token %}
                        {{ form|crispy }}
                        {% if redirect_field_value %}
                        <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}" />
                        {% endif %}
                        
                        <div class="d-grid gap-2 mt-4">
                            <button class="btn btn-primary" type="submit">{% trans "Sign In" %}</button>
                        </div>
                        
                        <div class="mt-3 text-center">
                            <a href="{% url 'account_reset_password' %}">{% trans "Forgot Password?" %}</a>
                        </div>
                        
                        <div class="mt-3 text-center">
                            <p class="mb-0">
                                {% trans "Don't have an account?" %}
                                <a href="{% url 'account_signup' %}">{% trans "Sign Up" %}</a>
                            </p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\account\logout.html
{% extends "base.html" %}
{% load static %}

{% block title %}Sign Out - KHCC AI Lab{% endblock %}

{% block content %}
<!-- Logout Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Sign Out</h1>
        <p class="lead">We hope to see you again soon!</p>
    </div>
</div>

<div class="container py-4">
    <div class="row justify-content-center">
        <div class="col-lg-6">
            <div class="card shadow-sm">
                <div class="card-body text-center py-5">
                    <i class="bi bi-box-arrow-right text-primary display-1 mb-4"></i>
                    <h2 class="h4 mb-4">Are you sure you want to sign out?</h2>
                    
                    <form method="post" action="{% url 'account_logout' %}">
                        {% csrf_token %}
                        {% if redirect_field_value %}
                        <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}"/>
                        {% endif %}
                        
                        <div class="d-flex justify-content-center gap-3">
                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-box-arrow-right me-2"></i>Yes, Sign Out
                            </button>
                            <a href="{% url 'projects:homepage' %}" class="btn btn-outline-secondary">
                                <i class="bi bi-x-circle me-2"></i>Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Quick Links -->
            <div class="text-center mt-4">
                <p class="text-muted mb-3">Quick Links</p>
                <div class="d-flex justify-content-center gap-3">
                    <a href="{% url 'projects:project_list' %}" class="btn btn-outline-primary btn-sm">
                        <i class="bi bi-grid me-2"></i>Browse Projects
                    </a>
                    <a href="{% url 'projects:help' %}" class="btn btn-outline-primary btn-sm">
                        <i class="bi bi-question-circle me-2"></i>Help Center
                    </a>
                </div>
            </div>

            <!-- Additional Info -->
            <div class="text-center mt-4">
                <p class="text-muted small mb-1">Having trouble? <a href="{% url 'projects:help' %}">Contact Support</a></p>
                <p class="text-muted small">
                    By signing out, your session will be ended securely.
                    <br>You can sign in again anytime.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- Newsletter Section -->
<div class="bg-light py-5 mt-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-6 text-center">
                <h3 class="h5 mb-4">Stay Connected</h3>
                <p class="text-muted mb-4">
                    Sign up for our newsletter to stay updated with the latest projects and research opportunities.
                </p>
                <div class="d-flex justify-content-center">
                    <a href="#" class="btn btn-outline-primary">
                        <i class="bi bi-envelope me-2"></i>Subscribe to Newsletter
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\account\signup.html
{% extends "base.html" %}
{% load i18n %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-body p-4 text-center">
                    <div class="mb-4">
                        <i class="bi bi-envelope-check text-success" style="font-size: 3rem;"></i>
                    </div>
                    
                    <h2 class="card-title text-center mb-4">{% trans "Verify Your Email Address" %}</h2>
                    
                    <p class="mb-4">
                        {% blocktrans %}
                        We have sent an email to verify your email address. 
                        Please check your inbox and click on the confirmation link to complete the registration.
                        {% endblocktrans %}
                    </p>
                    
                    <p class="text-muted small mb-4">
                        {% blocktrans %}
                        If you don't see the email in your inbox, please check your spam folder.
                        The confirmation link will expire in 24 hours.
                        {% endblocktrans %}
                    </p>
                    
                    <div class="mt-4">
                        <a href="{% url 'account_login' %}" class="btn btn-outline-primary">
                            {% trans "Return to Login" %}
                        </a>
                    </div>
                </div>
            </div>
            
            <div class="card mt-3 shadow">
                <div class="card-body p-3">
                    <h5 class="card-title h6 mb-3">{% trans "Need Help?" %}</h5>
                    <p class="card-text small mb-0">
                        {% blocktrans %}
                        If you're having trouble with the verification process, you can:
                        {% endblocktrans %}
                    </p>
                    <ul class="small mb-0">
                        <li>{% trans "Check your spam/junk folder" %}</li>
                        <li>{% trans "Make sure you entered the correct email address" %}</li>
                        <li>
                            <a href="{% url 'account_email' %}">
                                {% trans "Request a new verification email" %}
                            </a>
                        </li>
                        <li>
                            <a href="#">{% trans "Contact support" %}</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\account\verification_sent.html
{% extends "base.html" %}
{% load i18n %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-body p-4 text-center">
                    <div class="mb-4">
                        <i class="bi bi-envelope-check text-success" style="font-size: 3rem;"></i>
                    </div>
                    
                    <h2 class="card-title text-center mb-4">{% trans "Verify Your Email Address" %}</h2>
                    
                    <p class="mb-4">
                        {% blocktrans %}
                        We have sent an email to verify your email address. 
                        Please check your inbox and click on the confirmation link to complete the registration.
                        {% endblocktrans %}
                    </p>
                    
                    <p class="text-muted small mb-4">
                        {% blocktrans %}
                        If you don't see the email in your inbox, please check your spam folder.
                        The confirmation link will expire in 24 hours.
                        {% endblocktrans %}
                    </p>
                    
                    <div class="mt-4">
                        <a href="{% url 'account_login' %}" class="btn btn-outline-primary">
                            {% trans "Return to Login" %}
                        </a>
                    </div>
                </div>
            </div>
            
            <div class="card mt-3 shadow">
                <div class="card-body p-3">
                    <h5 class="card-title h6 mb-3">{% trans "Need Help?" %}</h5>
                    <p class="card-text small mb-0">
                        {% blocktrans %}
                        If you're having trouble with the verification process, you can:
                        {% endblocktrans %}
                    </p>
                    <ul class="small mb-0">
                        <li>{% trans "Check your spam/junk folder" %}</li>
                        <li>{% trans "Make sure you entered the correct email address" %}</li>
                        <li>
                            <a href="{% url 'account_email' %}">
                                {% trans "Request a new verification email" %}
                            </a>
                        </li>
                        <li>
                            <a href="#">{% trans "Contact support" %}</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\base.html
{% load static %}
{% load django_bootstrap5 %}
{% load crispy_forms_tags %}
{% load custom_filters %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}<a href="{% url 'projects:homepage' %}">KHCC AI Lab</a>{% endblock %}</title>
    
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
                <p>&copy; 2024 <a href="{% url 'projects:homepage' %}">KHCC AI Lab</a>. All rights reserved.</p>
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

# Contents from: .\emails\team_comment.html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .button { background: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        .footer { margin-top: 30px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h2>New Comment in {{ team.name }}</h2>
        <p>Hi {{ user.username }},</p>
        <p>{{ comment.author.username }} commented on the discussion "{{ comment.discussion.title }}":</p>
        
        <div style="background: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
            {{ comment.content|linebreaks }}
        </div>
        
        <p><a href="{{ site_url }}{% url 'discussion_detail' team.slug comment.discussion.id %}" class="button">View Comment</a></p>
        
        <div class="footer">
            <p>You received this email because you're a member of {{ team.name }}.</p>
            <p>To update your notification settings, visit your <a href="{{ site_url }}{% url 'team_settings' team.slug %}">team settings</a>.</p>
        </div>
    </div>
</body>
</html>

# Contents from: .\emails\team_discussion.html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .button { background: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        .footer { margin-top: 30px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h2>New Discussion in {{ team.name }}</h2>
        <p>Hi {{ user.username }},</p>
        <p>{{ discussion.author.username }} has started a new discussion in {{ team.name }}:</p>
        
        <h3>{{ discussion.title }}</h3>
        <p>{{ discussion.content|truncatewords:50 }}</p>
        
        <p><a href="{{ site_url }}{% url 'discussion_detail' team.slug discussion.id %}" class="button">View Discussion</a></p>
        
        <div class="footer">
            <p>You received this email because you're a member of {{ team.name }}.</p>
            <p>To update your notification settings, visit your <a href="{{ site_url }}{% url 'team_settings' team.slug %}">team settings</a>.</p>
        </div>
    </div>
</body>
</html>

# Contents from: .\emails\team_invitation.html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .button { background: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        .footer { margin-top: 30px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Invitation to Join {{ team.name }}</h2>
        <p>Hi {{ user.username }},</p>
        <p>{{ inviter.username }} has invited you to join their team {{ team.name }}.</p>
        
        <div style="background: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3>About {{ team.name }}</h3>
            <p>{{ team.description }}</p>
            
            {% if team.tags %}
            <p>Team focus: {{ team.tags }}</p>
            {% endif %}
            
            <p>Current members: {{ team.member_count }}</p>
        </div>
        
        <p><a href="{{ site_url }}{% url 'join_team' team.slug %}" class="button">Accept Invitation</a></p>
        
        <div class="footer">
            <p>If you don't want to join this team, you can simply ignore this email.</p>
        </div>
    </div>
</body>
</html>

# Contents from: .\emails\team_role_change.html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .button { background: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        .footer { margin-top: 30px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Role Update in {{ team.name }}</h2>
        <p>Hi {{ user.username }},</p>
        <p>Your role in {{ team.name }} has been updated to: <strong>{{ new_role }}</strong></p>
        
        {% if new_role == 'moderator' %}
        <p>As a moderator, you can now:</p>
        <ul>
            <li>Manage team discussions</li>
            <li>Moderate comments</li>
            <li>View team analytics</li>
        </ul>
        {% endif %}
        
        <p><a href="{{ site_url }}{% url 'team_detail' team.slug %}" class="button">View Team</a></p>
        
        <div class="footer">
            <p>You received this email because you're a member of {{ team.name }}.</p>
            <p>To update your notification settings, visit your <a href="{{ site_url }}{% url 'team_settings' team.slug %}">team settings</a>.</p>
        </div>
    </div>
</body>
</html>

# Contents from: .\errors.html
{% extends "base.html" %}

{% block title %}Error{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8 text-center">
            {% if error_code == 404 %}
                <h1 class="display-1">404</h1>
                <h2>Page Not Found</h2>
                <p>The page you are looking for does not exist or has been moved.</p>
            {% elif error_code == 403 %}
                <h1 class="display-1">403</h1> 
                <h2>Access Forbidden</h2>
                <p>You don't have permission to access this page.</p>
            {% elif error_code == 500 %}
                <h1 class="display-1">500</h1>
                <h2>Internal Server Error</h2>
                <p>Something went wrong on our end. Please try again later.</p>
            {% else %}
                <h1 class="display-1">Error</h1>
                <h2>Something Went Wrong</h2>
                <p>An unexpected error occurred. Please try again later.</p>
            {% endif %}

            {% if error_message %}
                <div class="alert alert-danger mt-3">
                    {{ error_message }}
                </div>
            {% endif %}

            <div class="mt-4">
                <a href="{% url 'home' %}" class="btn btn-primary">Return Home</a>
                <button onclick="history.back()" class="btn btn-secondary">Go Back</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}


# Contents from: .\help.html
{% extends 'base.html' %}
{% load static %}

{% block title %}Help & Manual - KHCC AI Lab{% endblock %}

{% block content %}
<!-- Help Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Help & Manual</h1>
        <p class="lead">Learn how to make the most of our platform's features and capabilities</p>
    </div>
</div>

<div class="container mb-5">
    <div class="row">
        <div class="col-lg-3">
            <!-- Navigation sidebar -->
            <div class="list-group sticky-top pt-3">
                <a href="#getting-started" class="list-group-item list-group-item-action">Getting Started</a>
                <a href="#seeds" class="list-group-item list-group-item-action">Seeds (Projects)</a>
                <a href="#teams" class="list-group-item list-group-item-action">Teams</a>
                <a href="#faculty" class="list-group-item list-group-item-action">Faculty</a>
                <a href="#talents" class="list-group-item list-group-item-action">Talents</a>
                <a href="#notifications" class="list-group-item list-group-item-action">Notifications</a>
            </div>
        </div>
        
        <div class="col-lg-9">
            <!-- Getting Started -->
            <section id="getting-started" class="mb-5">
                <h2 class="h3 mb-4">Getting Started</h2>
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">Welcome to KHCC AI Lab</h5>
                        <p>Our platform connects AI researchers, faculty members, and talented individuals in the field of artificial intelligence. Here's how to get started:</p>
                        <ol>
                            <li>Create an account or sign in using existing credentials</li>
                            <li>Complete your profile with relevant information</li>
                            <li>Explore Seeds (AI projects) or share your own</li>
                            <li>Join or create teams for collaboration</li>
                            <li>Connect with faculty members and other talents</li>
                        </ol>
                    </div>
                </div>
            </section>

            <!-- Seeds Section -->
            <section id="seeds" class="mb-5">
                <h2 class="h3 mb-4">Seeds (Projects)</h2>
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">Working with Seeds</h5>
                        <p>Seeds are AI projects that can be shared, collaborated on, and improved. You can:</p>
                        <ul>
                            <li>Browse and search existing Seeds</li>
                            <li>Submit new Seeds with GitHub repository links</li>
                            <li>Rate and bookmark interesting projects</li>
                            <li>Track project analytics and engagement</li>
                            <li>Collaborate with other researchers</li>
                        </ul>
                        
                        <div class="mt-3">
                            <h6>Key Features:</h6>
                            <ul>
                                <li><strong>Project Submission:</strong> Share your AI research and development work</li>
                                <li><strong>Analytics:</strong> Track views, engagement, and user interaction</li>
                                <li><strong>Collaboration:</strong> Comment, rate, and provide feedback</li>
                                <li><strong>Bookmarking:</strong> Save interesting projects for later reference</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Teams Section -->
            <section id="teams" class="mb-5">
                <h2 class="h3 mb-4">Teams</h2>
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">Team Collaboration</h5>
                        <p>Teams enable collaborative research and development:</p>
                        <ul>
                            <li>Create or join research teams</li>
                            <li>Manage team members and roles</li>
                            <li>Share projects within teams</li>
                            <li>Track team progress and contributions</li>
                        </ul>
                        
                        <div class="mt-3">
                            <h6>Team Roles:</h6>
                            <ul>
                                <li><strong>Founder:</strong> Creates and manages the team</li>
                                <li><strong>Moderator:</strong> Helps manage team activities</li>
                                <li><strong>Member:</strong> Participates in team projects</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Faculty Section -->
            <section id="faculty" class="mb-5">
                <h2 class="h3 mb-4">Faculty</h2>
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">Faculty Features</h5>
                        <p>Faculty members have additional capabilities:</p>
                        <ul>
                            <li>Create Gold Seed projects with rewards</li>
                            <li>Review and approve student submissions</li>
                            <li>Provide feedback and mentorship</li>
                            <li>Track student progress and engagement</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Talents Section -->
            <section id="talents" class="mb-5">
                <h2 class="h3 mb-4">Talents</h2>
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">Talent Network</h5>
                        <p>Connect with other AI enthusiasts and researchers:</p>
                        <ul>
                            <li>Create and customize your talent profile</li>
                            <li>Showcase your skills and projects</li>
                            <li>Follow other talents and track their work</li>
                            <li>Participate in collaborative projects</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Notifications Section -->
            <section id="notifications" class="mb-5">
                <h2 class="h3 mb-4">Notifications</h2>
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">Staying Updated</h5>
                        <p>Our notification system keeps you informed about:</p>
                        <ul>
                            <li>Comments and feedback on your projects</li>
                            <li>New followers and team invitations</li>
                            <li>Project ratings and bookmarks</li>
                            <li>Team updates and discussions</li>
                        </ul>
                        
                        <div class="mt-3">
                            <h6>Notification Settings:</h6>
                            <p>Customize your notification preferences in your profile settings to control what updates you receive.</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Support Section -->
            <section id="support" class="mb-5">
                <h2 class="h3 mb-4">Need Additional Help?</h2>
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">Support Resources</h5>
                        <p>If you need further assistance:</p>
                        <ul>
                            <li>Check our documentation for detailed guides</li>
                            <li>Reach out to team moderators</li>
                            <li>Contact faculty members for academic guidance</li>
                            <li>Use the platform's feedback features</li>
                        </ul>
                    </div>
                </div>
            </section>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\includes\navbar.html
<!-- templates/includes/navbar.html -->
<nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
    <div class="container">
        <a class="navbar-brand" href="{% url 'projects:homepage' %}">
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
                
                <li class="nav-item">
                    <a class="nav-link {% if active_tab == 'Faculty' %}active{% endif %}" 
                       href="{% url 'projects:faculty_page' %}">
                        <i class="bi bi-mortarboard me-1"></i>Faculty
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link {% if active_tab == 'Talents' %}active{% endif %}" 
                       href="{% url 'projects:talents' %}">
                        <i class="bi bi-person-hearts me-1"></i>Talents
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link {% if active_tab == 'Teams' %}active{% endif %}"
                       href="{% url 'projects:team_list' %}">
                        <i class="bi bi-people me-1"></i>Teams
                    </a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="resourcesDropdown" 
                       role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Resources
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="resourcesDropdown">
                        <li>
                            <a class="dropdown-item" href="{% url 'projects:tool_list' %}">
                                <i class="bi bi-tools me-2"></i>Tools
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="{% url 'projects:dataset_list' %}">
                                <i class="bi bi-database me-2"></i>Datasets
                            </a>
                        </li>
                        <li>
                            <hr class="dropdown-divider">
                        </li>
                        <li>
                            <a class="dropdown-item" href="{% url 'projects:startup_list' %}">
                                <i class="bi bi-building me-2"></i>Startups
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="{% url 'projects:sponsorship_list' %}">
                                <i class="bi bi-award me-2"></i>Sponsors
                            </a>
                        </li>
                    </ul>
                </li>
                <li class="nav-item">
                    <a class="nav-link {% if active_tab == 'Help' %}active{% endif %}"
                       href="{% url 'projects:help' %}">
                        <i class="bi bi-question-circle me-1"></i>Help
                    </a>
                </li>
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
                        <li>
                            <a class="dropdown-item" href="{% url 'projects:profile_settings' %}">
                                <i class="bi bi-gear"></i> Notification Settings
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

# Contents from: .\includes\pagination.html
<!-- templates/projects/includes/pagination.html -->
{% if page_obj.has_other_pages %}
<nav aria-label="Project pagination" class="my-4">
    <div class="d-flex justify-content-between align-items-center">
        <!-- Seeds per page dropdown -->
        <div class="me-3">
            <select class="form-select form-select-sm" id="seedsPerPage" onchange="updateSeedsPerPage(this.value)">
                <option value="12" {% if request.GET.per_page == '12' %}selected{% endif %}>12 per page</option>
                <option value="24" {% if request.GET.per_page == '24' %}selected{% endif %}>24 per page</option>
                <option value="48" {% if request.GET.per_page == '48' %}selected{% endif %}>48 per page</option>
            </select>
        </div>

        <!-- Existing pagination -->
        <ul class="pagination justify-content-center mb-0">
            {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?{% if request.GET.query %}query={{ request.GET.query }}&{% endif %}{% if request.GET.tags %}tags={{ request.GET.tags }}&{% endif %}{% if request.GET.sort %}sort={{ request.GET.sort }}&{% endif %}{% if request.GET.per_page %}per_page={{ request.GET.per_page }}&{% endif %}page=1" aria-label="First">
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
    </div>
</nav>
{% endif %}

<!-- Add this JavaScript at the bottom -->
<script>
function updateSeedsPerPage(value) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('per_page', value);
    urlParams.set('page', '1'); // Reset to first page when changing items per page
    window.location.href = `${window.location.pathname}?${urlParams.toString()}`;
}
</script>

# Contents from: .\projects\about.html
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

# Contents from: .\projects\application_form.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<!-- Application Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">
            {% if request.GET.type == 'sponsor' %}
                Sponsorship Application
            {% else %}
                Join Our Team
            {% endif %}
        </h1>
        <p class="lead">
            {% if request.GET.type == 'sponsor' %}
                Partner with us to advance AI in healthcare
            {% else %}
                Be part of our innovative research community
            {% endif %}
        </p>
    </div>
</div>

<!-- Application Form Section -->
<section class="application-form mb-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="card shadow-sm">
                    <div class="card-body p-4">
                        <form method="post" enctype="multipart/form-data">
                            {% csrf_token %}
                            {{ form.type }}
                            
                            <!-- Organization/Personal Details -->
                            <div class="mb-4">
                                <label class="form-label fw-bold">Name</label>
                                {{ form.name }}
                                {% if form.name.errors %}
                                    <div class="text-danger small">{{ form.name.errors }}</div>
                                {% endif %}
                            </div>
                            
                            <div class="mb-4">
                                <label class="form-label fw-bold">Email</label>
                                {{ form.email }}
                                {% if form.email.errors %}
                                    <div class="text-danger small">{{ form.email.errors }}</div>
                                {% endif %}
                            </div>
                            
                            {% if request.GET.type == 'sponsor' %}
                                <div class="mb-4">
                                    <label class="form-label fw-bold">Organization</label>
                                    {{ form.organization }}
                                </div>
                                
                                <div class="mb-4">
                                    <label class="form-label fw-bold">Sponsorship Level</label>
                                    {{ form.level }}
                                    <div class="form-text text-muted">
                                        Select your preferred sponsorship tier
                                    </div>
                                </div>
                            {% endif %}
                            
                            <!-- Message/Proposal -->
                            <div class="mb-4">
                                <label class="form-label fw-bold">Message</label>
                                {{ form.message }}
                                <div class="form-text text-muted">
                                    {% if request.GET.type == 'sponsor' %}
                                        Tell us about your organization and how you'd like to collaborate
                                    {% else %}
                                        Tell us about your background and interest in joining our team
                                    {% endif %}
                                </div>
                            </div>
                            
                            <!-- Attachments -->
                            <div class="mb-4">
                                <label class="form-label fw-bold">
                                    {% if request.GET.type == 'sponsor' %}
                                        Supporting Documents
                                    {% else %}
                                        Resume/CV
                                    {% endif %}
                                </label>
                                {{ form.attachment }}
                                <div class="form-text text-muted">
                                    PDF format preferred, max 10MB
                                </div>
                            </div>
                            
                            <!-- Submit Buttons -->
                            <div class="d-flex justify-content-center gap-3 mt-5">
                                <button type="submit" class="btn btn-primary px-4">
                                    Submit Application
                                </button>
                                <a href="{% url 'projects:homepage' %}" 
                                   class="btn btn-outline-secondary px-4">
                                    Cancel
                                </a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Contact Section -->
<section class="contact-us bg-light py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Questions?</h2>
                <p class="mb-4">
                    If you have any questions about the application process,
                    please don't hesitate to reach out.
                </p>
                <div class="d-flex justify-content-center gap-3">
                    <a href="mailto:contact@example.com" class="btn btn-outline-primary">
                        <i class="bi bi-envelope me-2"></i>Contact Us
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}

# Contents from: .\projects\application_forms.html

<!-- templates/projects/applications/application_form.html -->
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow">
                <div class="card-body">
                    <h2 class="card-title text-center mb-4">{{ application_type }} Application</h2>
                    
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label class="form-label">Application Type</label>
                            {{ form.type }}
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Resume/CV</label>
                            {{ form.resume }}
                            <div class="form-text">Upload your resume in PDF format (max 5MB)</div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Cover Letter</label>
                            {{ form.cover_letter }}
                            <div class="form-text">Tell us why you want to join KHCC AI Lab</div>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">
                                Submit Application
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

# Contents from: .\projects\dataset_form.html
<!-- templates/projects/datasets/dataset_form.html -->
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow">
                <div class="card-body">
                    <h2 class="card-title text-center mb-4">
                        {% if form.instance.pk %}
                            Edit Dataset
                        {% else %}
                            Add New Dataset
                        {% endif %}
                    </h2>
                    
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label class="form-label">Dataset Name</label>
                            {{ form.name }}
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Description</label>
                            {{ form.description }}
                            <div class="form-text">
                                Include information about data collection, format, and potential uses
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">File</label>
                            {{ form.file }}
                            <div class="form-text">Upload your dataset file (ZIP format recommended)</div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Format</label>
                                {{ form.format }}
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">License</label>
                                {{ form.license }}
                            </div>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">
                                {% if form.instance.pk %}
                                    Update Dataset
                                {% else %}
                                    Add Dataset
                                {% endif %}
                            </button>
                            <a href="{% url 'projects:dataset_list' %}" class="btn btn-outline-secondary">
                                Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>


# Contents from: .\projects\dataset_list.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<!-- Datasets Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Our Datasets</h1>
        <p class="lead">Access our curated collection of healthcare datasets</p>
    </div>
</div>

<!-- Datasets Section -->
<section class="datasets mb-5">
    <div class="container">
        <h2 class="h3 text-center mb-5">Available Datasets</h2>
        
        <div class="row g-4">
            {% for dataset in datasets %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <h3 class="h5 mb-2">{{ dataset.name }}</h3>
                        <p class="text-muted small mb-3">{{ dataset.description|truncatewords:30 }}</p>
                        <div class="d-flex justify-content-center gap-2 mb-3">
                            <span class="badge bg-primary">{{ dataset.format }}</span>
                            <span class="badge bg-secondary">{{ dataset.size|filesizeformat }}</span>
                            <span class="badge bg-info">{{ dataset.license }}</span>
                        </div>
                        <div class="d-flex justify-content-center gap-2">
                            <small class="text-muted me-2">{{ dataset.downloads }} downloads</small>
                            <a href="{% url 'projects:download_dataset' dataset.pk %}" class="btn btn-sm btn-primary">
                                <i class="bi bi-download me-1"></i>Download
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="col-12 text-center">
                <p class="text-muted">No datasets have been added yet.</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Contact Section -->
<section class="contact-us bg-light py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Need Help?</h2>
                <p class="mb-4">
                    Have questions about our datasets or need assistance?
                    We're here to help.
                </p>
                <div class="d-flex justify-content-center gap-3">
                    <a href="mailto:datasets@example.com" class="btn btn-outline-primary">
                        <i class="bi bi-envelope me-2"></i>Contact Support
                    </a>
                    <a href="{% url 'projects:help' %}" class="btn btn-primary">
                        <i class="bi bi-question-circle me-2"></i>Documentation
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}

# Contents from: .\projects\edit_profile.html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<!-- Banner -->
<div class="bg-primary py-4 mb-4">
    <div class="container">
        <h1 class="text-white">Profile Settings</h1>
        <p class="text-white-50 mb-0">Update your profile information and notification preferences</p>
    </div>
</div>

<div class="container py-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <!-- Profile Settings Card -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <h5 class="card-title mb-4">Profile Information</h5>
                    
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        {% if messages %}
                            {% for message in messages %}
                                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                                    {{ message }}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                </div>
                            {% endfor %}
                        {% endif %}

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

                        <!-- Notification Settings Card -->
                        <div class="card shadow-sm mb-4">
                            <div class="card-body">
                                <h5 class="card-title mb-4">Email Notification Preferences</h5>
                                
                                <div class="list-group mb-4">
                                    <!-- Comments -->
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">Comments on Your Seeds</h6>
                                            <p class="text-muted small mb-0">Receive emails when someone comments on your projects</p>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" name="email_on_comment" id="email_on_comment" {% if form.email_on_comment.value or True %}checked{% endif %}>
                                        </div>
                                    </div>

                                    <!-- Follows -->
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">New Followers</h6>
                                            <p class="text-muted small mb-0">Receive emails when someone follows you</p>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" name="email_on_follow" id="email_on_follow" {% if form.email_on_follow.value or True %}checked{% endif %}>
                                        </div>
                                    </div>

                                    <!-- Claps -->
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">Project Claps</h6>
                                            <p class="text-muted small mb-0">Receive emails when someone clap_count for your projects</p>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" name="email_on_clap" id="email_on_clap" {% if form.email_on_clap.value %}checked{% endif %}>
                                        </div>
                                    </div>

                                    <!-- Bookmarks -->
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">Project Bookmarks</h6>
                                            <p class="text-muted small mb-0">Receive emails when someone bookmarks your projects</p>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" name="email_on_bookmark" id="email_on_bookmark" {% if form.email_on_bookmark.value %}checked{% endif %}>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">
                                Save Changes
                            </button>
                            <a href="{% url 'projects:user_profile' username=user.username %}" 
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

# Contents from: .\projects\edit_project.html
<!-- templates/projects/edit_project.html -->
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Edit Project</h1>
    
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        
        <div class="row">
            <div class="col-md-8">
                <!-- Basic Project Info -->
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Project Information</h5>
                        {{ form.title|as_crispy_field }}
                        {{ form.description|as_crispy_field }}
                        {{ form.tags|as_crispy_field }}
                    </div>
                </div>
                
                <!-- Links -->
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Links</h5>
                        {{ form.github_link|as_crispy_field }}
                        {{ form.youtube_url|as_crispy_field }}
                    </div>
                </div>
                
                <!-- Files -->
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Files</h5>
                        {{ form.featured_image|as_crispy_field }}
                        {{ form.pdf_file|as_crispy_field }}
                        {{ form.additional_files|as_crispy_field }}
                    </div>
                </div>
                
                {% if 'Faculty' in user.groups.all|stringformat:'s' %}
                <!-- Gold Seed Settings (Faculty Only) -->
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3">
                            <i class="bi bi-trophy-fill text-warning"></i>
                            Gold Seed Settings
                        </h5>
                        <div class="form-check mb-3">
                            {{ form.is_gold }}
                            <label class="form-check-label" for="{{ form.is_gold.id_for_label }}">
                                Make this a Gold Seed
                            </label>
                            {% if form.is_gold.help_text %}
                                <small class="form-text text-muted">{{ form.is_gold.help_text }}</small>
                            {% endif %}
                        </div>
                        
                        <div class="gold-seed-options" {% if not form.instance.is_gold %}style="display: none;"{% endif %}>
                            {{ form.token_reward|as_crispy_field }}
                            {{ form.gold_goal|as_crispy_field }}
                            {{ form.deadline|as_crispy_field }}
                        </div>
                    </div>
                </div>
                {% endif %}
                
                <div class="card">
                    <div class="card-body">
                        <button type="submit" class="btn btn-primary w-100">
                            Save Changes
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </form>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const isGoldCheckbox = document.getElementById('{{ form.is_gold.id_for_label }}');
    const goldOptions = document.querySelector('.gold-seed-options');
    
    // Set initial state based on checkbox
    goldOptions.style.display = isGoldCheckbox.checked ? 'block' : 'none';
    
    isGoldCheckbox.addEventListener('change', function() {
        goldOptions.style.display = this.checked ? 'block' : 'none';
    });
});
</script>
{% endblock %}

# Contents from: .\projects\email.html
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

<p>Your project now has {{ project.clap_count }} clap_count in total.</p>

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

# Contents from: .\projects\faculty_page.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<!-- Faculty Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Our Faculty</h1>
        <p class="lead">Meet our distinguished team of researchers and educators</p>
    </div>
</div>

<!-- Core Faculty Section -->
<section class="core-faculty mb-5">
    <div class="container">
        <h2 class="h3 text-center mb-5">Core Faculty</h2>
        
        <div class="row g-4">
            {% for faculty in faculty_members %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <a href="{% url 'projects:user_profile' username=faculty.username %}">
                            <img src="{{ faculty.profile.avatar.url|default:'https://via.placeholder.com/150' }}" 
                                 alt="{{ faculty.get_full_name }}" 
                                 class="rounded-circle mb-3" 
                                 style="width: 150px; height: 150px; object-fit: cover;">
                            <h3 class="h5 mb-2">{{ faculty.get_full_name }}</h3>
                        </a>
                        <p class="text-primary small mb-2">{{ faculty.profile.title }}</p>
                        <p class="text-muted small mb-3">{{ faculty.profile.department }}</p>
                        <div class="d-flex justify-content-center gap-2">
                            {% if faculty.profile.linkedin_url %}
                            <a href="{{ faculty.profile.linkedin_url }}" class="text-dark" target="_blank">
                                <i class="bi bi-linkedin"></i>
                            </a>
                            {% endif %}
                            {% if faculty.profile.website %}
                            <a href="{{ faculty.profile.website }}" class="text-dark" target="_blank">
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
            {% empty %}
            <div class="col-12 text-center">
                <p class="text-muted">No faculty members found.</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Contact Section -->
<section class="contact-us bg-light py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Contact Us</h2>
                <p class="mb-4">
                    Have questions about our research or collaboration opportunities? 
                    We'd love to hear from you.
                </p>
                <div class="d-flex justify-content-center gap-3">
                    <a href="mailto:contact@example.com" class="btn btn-outline-primary">
                        <i class="bi bi-envelope me-2"></i>Email Us
                    </a>
                    <a href="{% url 'projects:faculty_page' %}#faculty" class="btn btn-primary">
                        <i class="bi bi-people me-2"></i>Meet the Team
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Join Us Section - Modified to remove careers link -->
<section class="join-us bg-light py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Join Our Faculty</h2>
                <p class="mb-4">
                    We're always looking for talented researchers and clinicians to join our team. 
                    If you're passionate about advancing AI in healthcare, we'd love to hear from you.
                </p>
                <!-- Replace careers link with contact information -->
                <a href="mailto:careers@example.com" class="btn btn-primary">
                    <i class="bi bi-envelope me-2"></i>Contact About Opportunities
                </a>
            </div>
        </div>
    </div>
</section>
{% endblock %}

# Contents from: .\projects\faq.html
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

# Contents from: .\projects\homepage.html
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
                <a href="{% url 'projects:submit_project' %}" class="btn btn-light btn-lg">
                    <i class="bi bi-plus-circle me-2"></i>Share Your Seed
                </a>
                {% endif %}
            </div>
            <div class="col-lg-6 d-none d-lg-block">
                <div class="text-center">
                    <!-- #Save this image in khcc_psut_ai_lab/static/images/collaboration.svg -->
                    <img src="{% static 'images/collaboration.jpeg' %}" alt="Collaboration" class="img-fluid" style="max-height: 400px;">
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
            <a href="{% url 'projects:project_list' %}" class="btn btn-link text-decoration-none">
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
                                    <i class="bi bi-hand-thumbs-up"></i> {{ project.clap_count }}
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
            <a href="{% url 'projects:project_list' %}?sort=-created_at" class="btn btn-link text-decoration-none">
                View All Seeds <i class="bi bi-arrow-right"></i>
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
                <img src="{% static 'images/khcc.jpg' %}" 
                     alt="King Hussein Cancer Center" 
                     class="img-fluid" 
                     style="max-height: 100px;">
            </div>
            <div class="col-md-4 text-center">
                <img src="{% static 'images/psut.jfif' %}" 
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
                <a href="{% url 'projects:submit_project' %}" class="btn btn-light btn-lg">
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

# Contents from: .\projects\leaderboard.html
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

# Contents from: .\projects\notification.html
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

# Contents from: .\projects\notifications.html
{% extends 'base.html' %}
{% load static %}

{% block title %}Notifications - KHCC AI Lab{% endblock %}

{% block content %}
<!-- Notifications Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Notifications</h1>
        <p class="lead">Stay updated with your latest activities and interactions</p>
    </div>
</div>

<div class="container py-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card shadow-sm">
                <div class="card-header bg-white d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Recent Notifications</h5>
                    {% if notifications %}
                    <a href="{% url 'projects:notifications' %}?mark_read=true" 
                       class="btn btn-sm btn-outline-primary">
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
                                 style="width: 40px; height: 40px; object-fit: cover;"
                                 alt="{{ notification.sender.username }}'s avatar">
                            <div class="flex-grow-1">
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <p class="mb-1">{{ notification.message }}</p>
                                        {% if notification.project and notification.notification_type == 'comment' %}
                                        <p class="text-muted small mb-1">
                                            <i class="bi bi-file-earmark-text me-1"></i>
                                            On project: <a href="{% url 'projects:project_detail' notification.project.id %}" class="text-decoration-none">{{ notification.project.title }}</a>
                                        </p>
                                        {% endif %}
                                    </div>
                                    <small class="text-muted ms-2">{{ notification.created_at|timesince }} ago</small>
                                </div>
                                <div class="mt-2">
                                    <a href="{% url 'projects:mark_notification_read' notification.id %}" 
                                       class="btn btn-sm btn-link px-0">
                                        {% if notification.project %}
                                            <i class="bi bi-arrow-right-circle me-1"></i>View Project
                                        {% elif notification.notification_type == 'follow' %}
                                            <i class="bi bi-person me-1"></i>View Profile
                                        {% else %}
                                            <i class="bi bi-eye me-1"></i>View
                                        {% endif %}
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% empty %}
                    <div class="list-group-item text-center py-5">
                        <i class="bi bi-bell text-muted display-4"></i>
                        <p class="text-muted mt-3 mb-0">No notifications yet</p>
                        <p class="text-muted small">
                            When you receive notifications, they will appear here
                        </p>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Quick Links Section -->
            <div class="mt-4 text-center">
                <div class="d-flex justify-content-center gap-3">
                    <a href="{% url 'projects:project_list' %}" class="btn btn-outline-primary">
                        <i class="bi bi-grid me-2"></i>Browse Projects
                    </a>
                    <a href="{% url 'projects:profile_settings' %}" class="btn btn-outline-primary">
                        <i class="bi bi-gear me-2"></i>Notification Settings
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\projects\profile_settings.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<!-- Banner -->
<div class="bg-primary py-4 mb-4">
    <div class="container">
        <h1 class="text-white">Notification Settings</h1>
        <p class="text-white-50 mb-0">Manage your email notification preferences</p>
    </div>
</div>

<div class="container py-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="card-title mb-4">Email Notification Preferences</h5>
                    
                    <form method="post">
                        {% csrf_token %}
                        
                        {% if messages %}
                            {% for message in messages %}
                                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                                    {{ message }}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                </div>
                            {% endfor %}
                        {% endif %}

                        <div class="list-group mb-4">
                            <!-- Comments -->
                            <div class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-1">Comments on Your Seeds</h6>
                                    <p class="text-muted small mb-0">Receive emails when someone comments on your projects</p>
                                </div>
                                <div class="form-check form-switch">
                                    {{ form.email_on_comment }}
                                </div>
                            </div>

                            <!-- Follows -->
                            <div class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-1">New Followers</h6>
                                    <p class="text-muted small mb-0">Receive emails when someone follows you</p>
                                </div>
                                <div class="form-check form-switch">
                                    {{ form.email_on_follow }}
                                </div>
                            </div>

                            <!-- Claps -->
                            <div class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-1">Project Claps</h6>
                                    <p class="text-muted small mb-0">Receive emails when someone clap_count for your projects</p>
                                </div>
                                <div class="form-check form-switch">
                                    {{ form.email_on_clap }}
                                </div>
                            </div>

                            <!-- Bookmarks -->
                            <div class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-1">Project Bookmarks</h6>
                                    <p class="text-muted small mb-0">Receive emails when someone bookmarks your projects</p>
                                </div>
                                <div class="form-check form-switch">
                                    {{ form.email_on_bookmark }}
                                </div>
                            </div>
                        </div>

                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">Save Preferences</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\projects\project_analytics.html
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
                                        <!-- Similar rows for clap_count, ratings, bookmarks -->
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

# Contents from: .\projects\project_detail.html
{% extends 'base.html' %}
{% load static %}
{% load humanize %}
{% load crispy_forms_tags %}
{% load custom_filters %}
{% load project_tags %}

{% block extra_css %}
<style>
    /* Base styles */
    :root {
        --transition-speed: 0.2s;
    }

    /* Image styles */
    .featured-image {
        max-height: 500px;
        object-fit: cover;
        width: 100%;
    }
    
    .featured-image-container img {
        max-height: 500px;
        width: 100%;
        object-fit: cover;
        transition: transform var(--transition-speed);
    }
    
    .featured-image-container img:hover {
        transform: scale(1.01);
    }

    /* Comment image styles */
    .comment-image {
        max-width: 300px;
        border-radius: 8px;
        cursor: pointer;
        transition: transform var(--transition-speed);
    }
    
    .comment-image:hover {
        transform: scale(1.02);
    }

    /* Card animations */
    .file-card {
        transition: transform var(--transition-speed);
    }
    
    .file-card:hover {
        transform: translateY(-2px);
    }

    /* Tag styles */
    .tag-badge {
        transition: all var(--transition-speed);
        background-color: #f8f9fa;
        color: #212529;
        text-decoration: none;
        padding: 0.35em 0.65em;
        border-radius: 0.25rem;
        display: inline-block;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .tag-badge:hover {
        background-color: var(--bs-primary);
        color: white;
        text-decoration: none;
    }

    /* Clap button styles */
    .clap-animation {
        animation: clap-jump 0.3s ease;
    }

    @keyframes clap-jump {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }

    .clap-button.active,
    .clap-comment-btn.active {
        background-color: var(--bs-primary);
        color: white;
    }

    .clap-button:hover,
    .clap-comment-btn:hover {
        transform: scale(1.05);
        transition: transform var(--transition-speed);
    }

    /* Comment thread styles */
    .comment-thread {
        margin-bottom: 1.5rem;
        border-bottom: 1px solid rgba(0,0,0,0.1);
        padding-bottom: 1.5rem;
    }

    .comment-thread:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }

    .comment-replies {
        margin-left: 2rem;
        padding-left: 1rem;
        border-left: 2px solid rgba(0,0,0,0.1);
    }

    .reply-form {
        margin-left: 2rem;
        margin-top: 1rem;
        padding: 1rem;
        background-color: rgba(0,0,0,0.02);
        border-radius: 0.5rem;
        display: none;
    }

    /* Modal styles */
    .modal-image {
        max-height: 90vh;
        width: auto;
        margin: 0 auto;
        display: block;
    }

    /* Utility classes */
    .cursor-pointer {
        cursor: pointer;
    }

    .object-fit-cover {
        object-fit: cover;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .comment-replies {
            margin-left: 1rem;
            padding-left: 0.5rem;
        }

        .reply-form {
            margin-left: 1rem;
        }
    }
</style>
{% endblock %}

{% block content %}
<!-- Toast Messages -->
<div class="toast-container position-fixed bottom-0 end-0 p-3">
    <div id="actionToast" class="toast" role="alert" aria-live="polite" aria-atomic="true">
        <div class="toast-header">
            <i class="bi bi-info-circle me-2"></i>
            <strong class="me-auto" id="toastTitle">Notification</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body" id="toastMessage"></div>
    </div>
</div>

<div class="container py-5">
    <div class="row">
        <!-- Main Content Column -->
        <div class="col-lg-8">
            <!-- Project Header Card -->
            <div class="card shadow-sm mb-4">
                {% if project.featured_image %}
                    <div class="featured-image-container position-relative">
                        <img src="{{ project.featured_image.url }}" 
                             alt="{{ project.title }}" 
                             class="featured-image card-img-top cursor-pointer"
                             data-bs-toggle="modal"
                             data-bs-target="#imageModal">
                {% endif %}
                
                <!-- Author Actions - Moved outside of featured_image block -->
                {% if user == project.author %}
                    <div class="position-absolute top-0 end-0 m-3">
                        <div class="dropdown">
                            <button class="btn btn-light btn-sm shadow-sm" type="button" data-bs-toggle="dropdown">
                                <i class="bi bi-three-dots-vertical"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li>
                                    <a href="{% url 'projects:edit_project' project.pk %}" class="dropdown-item">
                                        <i class="bi bi-pencil me-2"></i>Edit Project
                                    </a>
                                </li>
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
                    </div>
                {% endif %}
                
                {% if project.featured_image %}
                    </div>
                {% endif %}
                
                <div class="card-body">
                    <!-- Project Title and Author Info -->
                    <div class="d-flex justify-content-between align-items-start mb-4">
                        <div>
                            <h2 class="mb-2">{{ project.title }}</h2>
                            
                            <!-- Gold Seed Badge and Info -->
                            {% if project.is_gold %}
                            <div class="d-flex align-items-center gap-2 mb-3">
                                <span class="badge bg-warning text-dark d-flex align-items-center gap-1">
                                    <i class="bi bi-trophy-fill"></i> Gold Seed
                                </span>
                                {% if project.token_reward %}
                                <span class="badge bg-info d-flex align-items-center gap-1">
                                    <i class="bi bi-coin"></i> {{ project.token_reward }} Tokens
                                </span>
                                {% endif %}
                                {% if project.gold_goal %}
                                <span class="badge bg-secondary d-flex align-items-center gap-1">
                                    {% if project.gold_goal == 'all' %}
                                        <i class="bi bi-people-fill"></i> All Complete
                                    {% elif project.gold_goal == 'first' %}
                                        <i class="bi bi-lightning-fill"></i> First to Complete
                                    {% else %}
                                        <i class="bi bi-star-fill"></i> Best Solution
                                    {% endif %}
                                </span>
                                {% endif %}
                                {% if project.deadline %}
                                <span class="badge {% if project.can_submit %}bg-success{% else %}bg-danger{% endif %} d-flex align-items-center gap-1">
                                    <i class="bi bi-clock-fill"></i>
                                    {% if project.can_submit %}
                                        Deadline: {{ project.deadline|date:"M d, Y H:i" }}
                                    {% else %}
                                        Submissions Closed
                                    {% endif %}
                                </span>
                                {% endif %}
                            </div>
                            {% endif %}

                            <div class="d-flex align-items-center text-muted">
                                <a href="{% url 'projects:user_profile' project.author.username %}" 
                                   class="text-decoration-none text-muted">
                                    <img src="{% if project.author.profile.avatar %}{{ project.author.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ project.author.username }}{% endif %}" 
                                         alt="{{ project.author.username }}" 
                                         class="rounded-circle me-2"
                                         width="32" height="32">
                                    {{ project.author.get_full_name|default:project.author.username }}
                                </a>
                                <span class="mx-2">•</span>
                                <span>{{ project.created_at|naturaltime }}</span>
                                {% if project.updated_at > project.created_at %}
                                    <span class="mx-2">•</span>
                                    <span>Updated {{ project.updated_at|naturaltime }}</span>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                    
                    <!-- Project Title and Description -->
                    <div class="project-content mb-4">
                        {{ project.description|linebreaks }}
                    </div>

                    {% if project.is_gold %}
                        <div class="card mb-4 border-warning">
                            <div class="card-body">
                                <h5 class="card-title d-flex align-items-center gap-2">
                                    <i class="bi bi-trophy-fill text-warning"></i>
                                    Gold Seed Challenge
                                </h5>
                                <div class="mb-3">
                                    <strong>Reward:</strong> {{ project.token_reward }} Tokens
                                    <br>
                                    <strong>Goal:</strong> 
                                    {% if project.gold_goal == 'all' %}
                                        All participants who complete the challenge will receive tokens
                                    {% elif project.gold_goal == 'first' %}
                                        First participant to complete the challenge will receive tokens
                                    {% else %}
                                        Best solution will receive tokens
                                    {% endif %}
                                </div>
                                {% if project.can_submit %}
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div class="text-muted">
                                            <i class="bi bi-clock"></i> 
                                            Deadline: {{ project.deadline|date:"F d, Y H:i" }}
                                        </div>
                                        <a href="{% url 'projects:submit_solution' project.pk %}" 
                                           class="btn btn-warning">
                                            <i class="bi bi-trophy"></i> Submit Solution
                                        </a>
                                    </div>
                                {% else %}
                                    <div class="alert alert-danger mb-0">
                                        <i class="bi bi-exclamation-triangle-fill"></i>
                                        Submissions are now closed for this challenge.
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                    {% endif %}

                    {% if project.youtube_url %}
                        <div class="mb-4">
                            <div class="ratio ratio-16x9">
                                <iframe 
                                    src="{{ project.get_youtube_embed_url }}"
                                    title="Project Video"
                                    frameborder="0"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                    allowfullscreen>
                                </iframe>
                            </div>
                        </div>
                    {% endif %}

                    <!-- Tags Section -->
                    {% if project.tag_list %}
                        <div class="mb-4">
                            {% for tag in project.tag_list %}
                                <a href="{% url 'projects:project_list' %}?tags={{ tag }}" 
                                   class="tag-badge">
                                    <i class="bi bi-tag-fill me-1 small"></i>{{ tag }}
                                </a>
                            {% endfor %}
                        </div>
                    {% endif %}

                    <!-- Project Files Section -->
                    {% if project.pdf_file or project.additional_files %}
                        <div class="row g-3 mb-4">
                            {% if project.pdf_file %}
                                <div class="col-md-6">
                                    <div class="card h-100 file-card border">
                                        <div class="card-body text-center p-4">
                                            <i class="bi bi-file-pdf text-danger display-5 mb-3"></i>
                                            <h5 class="card-title h6 mb-2">Documentation</h5>
                                            <p class="text-muted small mb-3">
                                                PDF - {{ project.pdf_file.size|filesizeformat }}
                                            </p>
                                            <a href="{{ project.pdf_file.url }}" 
                                               class="btn btn-outline-primary btn-sm" 
                                               download>
                                                <i class="bi bi-download me-1"></i>Download PDF
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            {% endif %}  

                            {% if project.additional_files %}
                                <div class="col-md-6">
                                    <div class="card h-100 file-card border">
                                        <div class="card-body text-center p-4">
                                            <i class="bi bi-file-earmark-zip text-primary display-5 mb-3"></i>
                                            <h5 class="card-title h6 mb-2">Project Files</h5>
                                            <p class="text-muted small mb-3">
                                                {{ project.additional_files.name|split:'/'|last }}
                                                ({{ project.additional_files.size|filesizeformat }})
                                            </p>
                                            <a href="{{ project.additional_files.url }}" 
                                               class="btn btn-outline-primary btn-sm"
                                               download>
                                                <i class="bi bi-download me-1"></i>Download Files
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            {% endif %}
                        </div>
                    {% endif %}

                    <!-- Action Buttons Section -->
                    <div class="d-flex flex-wrap justify-content-between align-items-center gap-2">
                        <div class="d-flex flex-wrap gap-2">
                            {% if project.github_link %}
                                <a href="{{ project.github_link }}" 
                                   target="_blank" 
                                   class="btn btn-dark">
                                    <i class="bi bi-github me-2"></i>View on GitHub
                                </a>
                            {% endif %}
                            
                            {% if user.is_authenticated %}
                                <button id="clap-btn" 
                                        class="btn btn-outline-primary clap-button {% if user_interactions.has_clapped %}active{% endif %}"
                                        data-project-id="{{ project.id }}">
                                    <i class="bi bi-hands-clapping me-1"></i>
                                    <span id="clap-count">{{ project.clap_count }}</span>
                                </button>
                                
                                <button class="btn btn-outline-primary bookmark-btn" 
                                        data-project-id="{{ project.id }}"
                                        {% if user_interactions.bookmark %}data-bookmarked="true"{% endif %}>
                                    <i class="bi bi-bookmark{% if user_interactions.bookmark %}-fill{% endif %}"></i>
                                </button>
                            {% endif %}
                        </div>
                        
                        <!-- Share Button -->
                        <div class="dropdown">
                            <button class="btn btn-outline-secondary dropdown-toggle" 
                                    type="button" 
                                    data-bs-toggle="dropdown">
                                <i class="bi bi-share me-1"></i>Share
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li>
                                    <button class="dropdown-item copy-link" 
                                            data-url="{{ request.build_absolute_uri }}">
                                        <i class="bi bi-link-45deg me-2"></i>Copy Link
                                    </button>
                                </li>
                                <li>
                                    <a class="dropdown-item" 
                                       href="https://twitter.com/intent/tweet?text={{ project.title|urlencode }}&url={{ request.build_absolute_uri|urlencode }}" 
                                       target="_blank">
                                        <i class="bi bi-twitter me-2"></i>Share on Twitter
                                    </a>
                                </li>
                                <li>
                                    <a class="dropdown-item" 
                                       href="https://www.linkedin.com/shareArticle?mini=true&url={{ request.build_absolute_uri|urlencode }}&title={{ project.title|urlencode }}" 
                                       target="_blank">
                                        <i class="bi bi-linkedin me-2"></i>Share on LinkedIn
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Comments Section -->
            <div class="card shadow-sm">
                <div class="card-header bg-white d-flex justify-content-between align-items-center">
                    <h4 class="card-title mb-0">Discussion</h4>
                    <span class="badge bg-secondary">{{ project.comments.count }}</span>
                </div>
                
                <div class="card-body">
                    <!-- Comment Form -->
                    {% if user.is_authenticated %}
                        <form method="post" 
                              action="{% url 'projects:project_detail' project.pk %}" 
                              enctype="multipart/form-data" 
                              class="mb-4 comment-form"
                              id="main-comment-form">
                            {% csrf_token %}
                            {{ comment_form|crispy }}
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <div class="form-text">
                                    <i class="bi bi-image me-1"></i>
                                    You can attach an image to your comment
                                </div>
                                <button type="submit" class="btn btn-primary">
                                    Post Comment
                                </button>
                            </div>
                        </form>
                    {% else %}
                        <div class="alert alert-info d-flex align-items-center" role="alert">
                            <i class="bi bi-info-circle me-2"></i>
                            <div>
                                Please <a href="{% url 'login' %}?next={{ request.path }}" class="alert-link">sign in</a> 
                                to join the discussion.
                            </div>
                        </div>
                    {% endif %}
                    
                    <!-- Comments List -->
                    <div class="comments-list">
                        {% for comment in comments %}
                            <div class="comment-thread" id="comment-{{ comment.id }}">
                                <!-- Parent Comment -->
                                <div class="card border-0 bg-light">
                                    <div class="card-body">
                                        <!-- Comment Header -->
                                        <div class="d-flex align-items-start mb-3">
                                            <img src="{% if comment.user.profile.avatar %}{{ comment.user.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ comment.user.username }}{% endif %}" 
                                                 alt="{{ comment.user.username }}" 
                                                 class="rounded-circle me-2"
                                                 width="32" height="32">
                                            <div>
                                                <div class="d-flex align-items-center">
                                                    <a href="{% url 'projects:user_profile' comment.user.username %}" 
                                                       class="fw-bold text-decoration-none text-dark me-2">
                                                        {{ comment.user.username }}
                                                    </a>
                                                    {% if comment.user == project.author %}
                                                        <span class="badge bg-primary">Author</span>
                                                    {% endif %}
                                                </div>
                                                <div class="text-muted small">
                                                    {{ comment.created_at|naturaltime }}
                                                    {% if comment.updated_at > comment.created_at %}
                                                        • edited {{ comment.updated_at|naturaltime }}
                                                    {% endif %}
                                                </div>
                                            </div>
                                        </div>
                                        
                                        <!-- Comment Content -->
                                        <div class="comment-content mb-3">
                                            {{ comment.content|linebreaks }}
                                            {% if comment.image %}
                                                <img src="{{ comment.image.url }}" 
                                                     alt="Comment image" 
                                                     class="comment-image mt-2"
                                                     data-bs-toggle="modal"
                                                     data-bs-target="#imageModal"
                                                     data-full-image="{{ comment.image.url }}">
                                            {% endif %}
                                        </div>
                                        
                                        <!-- Comment Actions -->
                                        {% if user.is_authenticated %}
                                            <div class="d-flex gap-2">
                                                <!-- Clap Button -->
                                                <button class="btn btn-sm btn-light clap-comment-btn {% if comment.has_user_clapped %}active{% endif %}"
                                                        data-comment-id="{{ comment.id }}">
                                                    <i class="bi bi-hands-clapping me-1"></i>
                                                    <span class="clap-count">{{ comment.clap_count }}</span>
                                                </button>
                                                
                                                <!-- Reply Button -->
                                                <button class="btn btn-sm btn-light reply-btn" 
                                                        data-comment-id="{{ comment.id }}">
                                                    <i class="bi bi-reply me-1"></i>Reply
                                                </button>
                                                
                                                <!-- Delete Button (for comment author or project author) -->
                                                {% if user == comment.user or user == project.author %}
                                                    <button class="btn btn-sm btn-light text-danger delete-comment-btn" 
                                                            data-comment-id="{{ comment.id }}"
                                                            data-url="{% url 'projects:delete_comment' comment.id %}">
                                                        <i class="bi bi-trash me-1"></i>Delete
                                                    </button>
                                                {% endif %}
                                            </div>
                                        {% endif %}
                                    </div>
                                </div>
                                
                                <!-- Reply Form -->
                                <div class="reply-form" id="reply-form-{{ comment.id }}">
                                    <form method="post" 
                                          action="{% url 'projects:project_detail' project.pk %}" 
                                          enctype="multipart/form-data">
                                        {% csrf_token %}
                                        <input type="hidden" name="parent_id" value="{{ comment.id }}">
                                        {{ comment_form|crispy }}
                                        <div class="d-flex justify-content-end gap-2 mt-3">
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
                                    <div class="comment-replies mt-3">
                                        {% for reply in comment.replies.all %}
                                            <div class="card border-0 bg-light mb-2" id="comment-{{ reply.id }}">
                                                <div class="card-body">
                                                    <!-- Reply Header -->
                                                    <div class="d-flex align-items-start mb-2">
                                                        <img src="{% if reply.user.profile.avatar %}{{ reply.user.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ reply.user.username }}{% endif %}" 
                                                             alt="{{ reply.user.username }}" 
                                                             class="rounded-circle me-2"
                                                             width="24" height="24">
                                                        <div>
                                                            <div class="d-flex align-items-center">
                                                                <a href="{% url 'projects:user_profile' reply.user.username %}" 
                                                                   class="fw-bold text-decoration-none text-dark me-2">
                                                                    {{ reply.user.username }}
                                                                </a>
                                                                {% if reply.user == project.author %}
                                                                    <span class="badge bg-primary">Author</span>
                                                                {% endif %}
                                                            </div>
                                                            <div class="text-muted small">
                                                                {{ reply.created_at|naturaltime }}
                                                            </div>
                                                        </div>
                                                    </div>
                                                    
                                                    <!-- Reply Content -->
                                                    <div class="reply-content mb-2">
                                                        {{ reply.content|linebreaks }}
                                                        {% if reply.image %}
                                                            <img src="{{ reply.image.url }}" 
                                                                 alt="Reply image" 
                                                                 class="comment-image mt-2"
                                                                 data-bs-toggle="modal"
                                                                 data-bs-target="#imageModal"
                                                                 data-full-image="{{ reply.image.url }}">
                                                        {% endif %}
                                                    </div>
                                                    
                                                    <!-- Reply Actions -->
                                                    {% if user.is_authenticated %}
                                                        <div class="d-flex gap-2">
                                                            <button class="btn btn-sm btn-light clap-comment-btn {% if reply.has_user_clapped %}active{% endif %}"
                                                                    data-comment-id="{{ reply.id }}">
                                                                <i class="bi bi-hands-clapping me-1"></i>
                                                                <span class="clap-count">{{ reply.clap_count }}</span>
                                                            </button>
                                                            
                                                            {% if user == reply.user or user == project.author %}
                                                                <button class="btn btn-sm btn-light text-danger delete-comment-btn" 
                                                                        data-comment-id="{{ reply.id }}"
                                                                        data-url="{% url 'projects:delete_comment' reply.id %}">
                                                                    <i class="bi bi-trash me-1"></i>Delete
                                                                </button>
                                                            {% endif %}
                                                        </div>
                                                    {% endif %}
                                                </div>
                                            </div>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        {% empty %}
                            <div class="text-center py-5">
                                <i class="bi bi-chat-dots text-muted display-4"></i>
                                <p class="text-muted mt-3 mb-0">No comments yet. Be the first to share your thoughts!</p>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>

        <!-- Sidebar -->
        <div class="col-lg-4">
            <div class="sticky-sidebar">
                <!-- Project Stats Card -->
                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-4">Project Statistics</h5>
                        <div class="row g-3">
                            <!-- Claps Stat -->
                            <div class="col-6">
                                <div class="d-flex align-items-start">
                                    <div class="stats-icon rounded p-2 me-3 bg-primary-subtle">
                                        <i class="bi bi-hands-clapping text-primary"></i>
                                    </div>
                                    <div>
                                        <small class="text-muted d-block">Claps</small>
                                        <span class="fs-5 fw-semibold stats-claps">{{ stats.clap_count }}</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Comments Stat -->
                            <div class="col-6">
                                <div class="d-flex align-items-start">
                                    <div class="stats-icon rounded p-2 me-3 bg-primary-subtle">
                                        <i class="bi bi-chat-dots text-primary"></i>
                                    </div>
                                    <div>
                                        <small class="text-muted d-block">Comments</small>
                                        <span class="fs-5 fw-semibold">{{ project.comments.count }}</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Rating Stat -->
                            <div class="col-6">
                                <div class="d-flex align-items-start">
                                    <div class="stats-icon rounded p-2 me-3 bg-primary-subtle">
                                        <i class="bi bi-star text-primary"></i>
                                    </div>
                                    <div>
                                        <small class="text-muted d-block">Avg Rating</small>
                                        <span class="fs-5 fw-semibold">{{ project.average_rating|default:"--" }}</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Views Stat -->
                            <div class="col-6">
                                <div class="d-flex align-items-start">
                                    <div class="stats-icon rounded p-2 me-3 bg-primary-subtle">
                                        <i class="bi bi-eye text-primary"></i>
                                    </div>
                                    <div>
                                        <small class="text-muted d-block">Views</small>
                                        <span class="fs-5 fw-semibold">{{ stats.view_count|default:"0" }}</span>
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
                                <h6 class="mb-1">
                                    <a href="{% url 'projects:user_profile' project.author.username %}" 
                                       class="text-decoration-none text-dark">
                                        {{ project.author.get_full_name|default:project.author.username }}
                                    </a>
                                </h6>
                                {% if project.author.profile.title %}
                                    <p class="text-muted small mb-0">{{ project.author.profile.title }}</p>
                                {% endif %}
                                {% if project.author.profile.department %}
                                    <p class="text-muted small mb-0">{{ project.author.profile.department }}</p>
                                {% endif %}
                            </div>
                        </div>

                        {% if project.author.profile.bio %}
                            <p class="small mb-3">{{ project.author.profile.bio }}</p>
                        {% endif %}

                        {% if project.author.profile.location %}
                            <div class="d-flex align-items-center mb-3">
                                <i class="bi bi-geo-alt text-muted me-2"></i>
                                <span class="small text-muted">{{ project.author.profile.location }}</span>
                            </div>
                        {% endif %}

                        <!-- Social Links -->
                        <div class="d-flex gap-2 mb-3">
                            {% if project.author.profile.github_username %}
                                <a href="https://github.com/{{ project.author.profile.github_username }}" 
                                   class="btn btn-sm btn-dark" 
                                   target="_blank">
                                    <i class="bi bi-github"></i>
                                </a>
                            {% endif %}
                            
                            {% if project.author.profile.linkedin_url %}
                                <a href="{{ project.author.profile.linkedin_url }}" 
                                   class="btn btn-sm btn-primary" 
                                   target="_blank">
                                    <i class="bi bi-linkedin"></i>
                                </a>
                            {% endif %}

                            {% if project.author.profile.twitter_username %}
                                <a href="https://twitter.com/{{ project.author.profile.twitter_username }}" 
                                   class="btn btn-sm btn-info" 
                                   target="_blank">
                                    <i class="bi bi-twitter text-white"></i>
                                </a>
                            {% endif %}
                        </div>

                        <div class="d-flex justify-content-between text-muted small">
                            <span>Projects: {{ project.author.projects.count }}</span>
                            <span>Member since: {{ project.author.date_joined|date:"M Y" }}</span>
                        </div>
                    </div>
                </div>

                <!-- Similar Projects Card -->
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title mb-4">Similar Projects</h5>
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
                                    <div class="d-flex align-items-center">
                                        <img src="{% if similar.author.profile.avatar %}{{ similar.author.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ similar.author.username }}{% endif %}" 
                                             alt="{{ similar.author.username }}" 
                                             class="rounded-circle me-2"
                                             width="20" height="20">
                                        <span class="text-muted">{{ similar.author.username }}</span>
                                    </div>
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
</div>

<!-- Modals -->
<!-- Image Modal -->
<div class="modal fade" id="imageModal" tabindex="-1">
    <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content bg-dark">
            <div class="modal-body p-0 position-relative">
                <button type="button" 
                        class="btn-close btn-close-white position-absolute top-0 end-0 m-3" 
                        data-bs-dismiss="modal"></button>
                <img src="" class="img-fluid w-100" id="modalImage" alt="Full size image">
            </div>
        </div>
    </div>
</div>

<!-- Delete Comment Modal -->
<div class="modal fade" id="deleteCommentModal" tabindex="-1">
    <div class="modal-dialog modal-sm modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Delete Comment</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p class="mb-0">Are you sure you want to delete this comment? This action cannot be undone.</p>
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
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Delete Project</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="alert alert-danger">
                    <h6 class="alert-heading fw-bold mb-1">Warning</h6>
                    <p class="mb-0">This action will permanently delete:</p>
                    <ul class="mb-0 mt-2">
                        <li>All project files and images</li>
                        <li>All comments and discussions</li>
                        <li>All analytics data</li>
                        <li>All associated notifications</li>
                    </ul>
                </div>
                <p class="mb-0">Are you sure you want to proceed? This action cannot be undone.</p>
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
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));

        // Initialize toast
        const actionToast = new bootstrap.Toast(document.getElementById('actionToast'));

        // Show toast message function
        function showToast(title, message, delay = 3000) {
            const toast = document.getElementById('actionToast');
            toast.querySelector('#toastTitle').textContent = title;
            toast.querySelector('#toastMessage').textContent = message;
            const bsToast = bootstrap.Toast.getInstance(toast) || new bootstrap.Toast(toast, { delay: delay });
            bsToast.show();
        }

        // Handle clap button for project
        $('#clap-btn').click(function() {
            const btn = $(this);
            const projectId = btn.data('project-id');
            
            $.post("{% url 'projects:clap_project' project.pk %}", {
                csrfmiddlewaretoken: '{{ csrf_token }}'
            })
            .done(function(response) {
                if (response.status === 'success' || response.status === 'removed') {
                    $('#clap-count').text(response.claps);
                    btn.toggleClass('active');
                    
                    // Add animation
                    btn.addClass('clap-animation');
                    setTimeout(() => btn.removeClass('clap-animation'), 300);
                    
                    // Update stats card
                    $('.stats-claps').text(response.claps);
                }
            })
            .fail(function() {
                showToast('Error', 'Failed to update clap. Please try again.');
            });
        });

        // Handle comment claps
        $('.clap-comment-btn').click(function() {
            const btn = $(this);
            const commentId = btn.data('comment-id');
            
            $.post(`/comment/${commentId}/clap/`, {
                csrfmiddlewaretoken: '{{ csrf_token }}'
            })
            .done(function(response) {
                if (response.status === 'success' || response.status === 'removed') {
                    btn.find('.clap-count').text(response.claps);
                    btn.toggleClass('active');
                    
                    // Add animation
                    btn.addClass('clap-animation');
                    setTimeout(() => btn.removeClass('clap-animation'), 300);
                }
            })
            .fail(function() {
                showToast('Error', 'Failed to update clap. Please try again.');
            });
        });

        // Handle reply functionality
        $('.reply-btn').click(function() {
            const commentId = $(this).data('comment-id');
            $('.reply-form').not(`#reply-form-${commentId}`).slideUp();
            $(`#reply-form-${commentId}`).slideToggle();
        });

        $('.cancel-reply').click(function() {
            $(this).closest('.reply-form').slideUp();
        });

        // Handle comment deletion
        let commentToDelete = null;
        let deleteUrl = null;

        $('.delete-comment-btn').click(function() {
            commentToDelete = $(this).data('comment-id');
            deleteUrl = $(this).data('url');
            $('#deleteCommentModal').modal('show');
        });

        $('#confirmDeleteComment').click(function() {
            if (commentToDelete && deleteUrl) {
                $.post(deleteUrl, {
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                })
                .done(function(response) {
                    if (response.status === 'success') {
                        $(`#comment-${commentToDelete}`).fadeOut(300, function() {
                            $(this).remove();
                            showToast('Success', 'Comment deleted successfully');
                        });
                    }
                })
                .fail(function() {
                    showToast('Error', 'Failed to delete comment. Please try again.');
                });
                $('#deleteCommentModal').modal('hide');
            }
        });

        // Handle bookmark toggle
        $('.bookmark-btn').click(function() {
            const btn = $(this);
            
            $.post("{% url 'projects:bookmark_project' project.pk %}", {
                csrfmiddlewaretoken: '{{ csrf_token }}'
            })
            .done(function(response) {
                btn.find('i').toggleClass('bi-bookmark bi-bookmark-fill');
                showToast('Success', response.message);
            })
            .fail(function() {
                showToast('Error', 'Failed to update bookmark. Please try again.');
            });
        });

        // Handle image modal
        $('.comment-image').click(function() {
            const fullImage = $(this).data('full-image');
            $('#modalImage').attr('src', fullImage);
        });

        // Handle link copying
        $('.copy-link').click(function() {
            const url = $(this).data('url');
            navigator.clipboard.writeText(url)
                .then(() => showToast('Success', 'Link copied to clipboard!'))
                .catch(() => showToast('Error', 'Failed to copy link. Please try again.'));
        });

        // Smooth scroll to comment if URL has comment ID
        if (window.location.hash && window.location.hash.includes('comment-')) {
            const commentId = window.location.hash;
            $(commentId)[0]?.scrollIntoView({ behavior: 'smooth', block: 'center' });
            $(commentId).addClass('bg-light');
            setTimeout(() => $(commentId).removeClass('bg-light'), 2000);
        }
    });
</script>
{% endblock %}





# Contents from: .\projects\project_list.html
{% extends 'base.html' %}
{% load static %}
{% load crispy_forms_tags %}
{% load query_tags %}  {# Add this line to load the custom template tags #}


{% block content %}
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Seeds</h1>
        <p class="lead">Discover innovative AI projects and connect with fellow developers</p>
    </div>
</div>

<div class="container my-4">
    <div class="row g-4">
        <!-- Filters Sidebar -->
        <div class="col-md-3">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="card-title mb-4">Filter Seeds</h5>
                    <form method="GET" id="filterForm">
                        <!-- Search Bar -->
                        <div class="mb-4">
                            <div class="input-group">
                                <input type="text" 
                                       name="query" 
                                       class="form-control" 
                                       placeholder="Search seeds..."
                                       value="{{ request.GET.query|default:'' }}">
                                <button class="btn btn-outline-secondary" type="submit">
                                    <i class="bi bi-search"></i>
                                </button>
                            </div>
                        </div>

                        <!-- Seed Categories -->
                        <div class="mb-4">
                            <label class="form-label fw-bold">Categories</label>
                            <div class="d-grid gap-2">
                                <input type="radio" 
                                       class="btn-check" 
                                       name="category" 
                                       id="all" 
                                       value="all"
                                       {% if not request.GET.category or request.GET.category == 'all' %}checked{% endif %}>
                                <label class="btn btn-outline-secondary" for="all">
                                    <i class="bi bi-grid-fill me-2"></i>All Seeds
                                </label>

                                <input type="radio" 
                                       class="btn-check" 
                                       name="category" 
                                       id="featured" 
                                       value="featured"
                                       {% if request.GET.category == 'featured' %}checked{% endif %}>
                                <label class="btn btn-outline-primary" for="featured">
                                    <i class="bi bi-star-fill me-2"></i>Featured Seeds
                                </label>

                                <input type="radio" 
                                       class="btn-check" 
                                       name="category" 
                                       id="gold" 
                                       value="gold"
                                       {% if request.GET.category == 'gold' %}checked{% endif %}>
                                <label class="btn btn-outline-warning" for="gold">
                                    <i class="bi bi-trophy-fill me-2"></i>Gold Seeds
                                </label>

                                <input type="radio" 
                                       class="btn-check" 
                                       name="category" 
                                       id="latest" 
                                       value="latest"
                                       {% if request.GET.category == 'latest' %}checked{% endif %}>
                                <label class="btn btn-outline-success" for="latest">
                                    <i class="bi bi-clock-fill me-2"></i>Latest Seeds
                                </label>

                                <input type="radio" 
                                       class="btn-check" 
                                       name="category" 
                                       id="popular" 
                                       value="popular"
                                       {% if request.GET.category == 'popular' %}checked{% endif %}>
                                <label class="btn btn-outline-info" for="popular">
                                    <i class="bi bi-heart-fill me-2"></i>Popular Seeds
                                </label>
                            </div>
                        </div>

                        <!-- Tags -->
                        <div class="mb-4">
                            <label class="form-label fw-bold">Tags</label>
                            <div class="tag-cloud">
                                {% for tag in popular_tags %}
                                <div class="form-check">
                                    <input class="form-check-input" 
                                           type="checkbox" 
                                           name="tags" 
                                           value="{{ tag }}"
                                           id="tag_{{ forloop.counter }}"
                                           {% if tag in selected_tags %}checked{% endif %}>
                                    <label class="form-check-label" for="tag_{{ forloop.counter }}">
                                        {{ tag }}
                                    </label>
                                </div>
                                {% endfor %}
                            </div>
                        </div>

                        <!-- Sort -->
                        <div class="mb-4">
                            <label class="form-label fw-bold">Sort By</label>
                            <select class="form-select" name="sort">
                                <option value="-created_at" {% if request.GET.sort == '-created_at' %}selected{% endif %}>
                                    Newest First
                                </option>
                                <option value="created_at" {% if request.GET.sort == 'created_at' %}selected{% endif %}>
                                    Oldest First
                                </option>
                                <option value="-clap_count" {% if request.GET.sort == '-clap_count' %}selected{% endif %}>
                                    Most Popular
                                </option>
                                <option value="-rating_avg" {% if request.GET.sort == '-rating_avg' %}selected{% endif %}>
                                    Highest Rated
                                </option>
                            </select>
                        </div>

                        <button type="submit" class="btn btn-primary w-100">
                            Apply Filters
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Projects Grid -->
        <div class="col-md-9">
            <!-- Active Filters Display -->
            {% if request.GET %}
            <div class="mb-4">
                <h6 class="text-muted mb-2">Active Filters:</h6>
                <div class="d-flex flex-wrap gap-2">
                    {% if request.GET.query %}
                    <span class="badge bg-light text-dark">
                        Search: {{ request.GET.query }}
                        <a href="?{% query_transform request.GET 'query' '' %}" class="text-dark text-decoration-none ms-2">×</a>
                    </span>
                    {% endif %}

                    {% if request.GET.category and request.GET.category != 'all' %}
                    <span class="badge bg-light text-dark">
                        Category: {{ request.GET.category|title }}
                        <a href="?{% query_transform request.GET 'category' '' %}" class="text-dark text-decoration-none ms-2">×</a>
                    </span>
                    {% endif %}

                    {% for tag in selected_tags %}
                    <span class="badge bg-light text-dark">
                        Tag: {{ tag }}
                        <a href="?{% query_transform request.GET 'tags' tag 'remove' %}" class="text-dark text-decoration-none ms-2">×</a>
                    </span>
                    {% endfor %}

                    {% if request.GET %}
                    <a href="{% url 'projects:project_list' %}" class="btn btn-sm btn-outline-secondary">
                        Clear All Filters
                    </a>
                    {% endif %}
                </div>
            </div>
            {% endif %}

            <!-- Projects Grid -->
            <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                {% for project in page_obj %}
                <div class="col">
                    <div class="card h-100 shadow-sm project-card">
                        <!-- Badges -->
                        <div class="card-badges">
                            {% if project.is_featured %}
                            <span class="badge bg-primary position-absolute top-0 start-0 m-2">
                                <i class="bi bi-star-fill"></i>
                            </span>
                            {% endif %}
                            
                            {% if project.is_gold %}
                            <span class="badge bg-warning text-dark position-absolute top-0 end-0 m-2">
                                <i class="bi bi-trophy-fill me-1"></i>{{ project.token_reward }}
                            </span>
                            {% endif %}
                        </div>

                        <!-- Only show image section if image exists -->
                        {% if project.featured_image %}
                        <img src="{{ project.featured_image.url }}" 
                             class="card-img-top"
                             alt="{{ project.title }}"
                             style="height: 140px; object-fit: cover;">
                        {% endif %}

                        <div class="card-body">
                            <h6 class="card-title mb-1">
                                <a href="{% url 'projects:project_detail' project.pk %}" 
                                   class="text-decoration-none text-dark stretched-link">
                                    {{ project.title }}
                                </a>
                            </h6>

                            {% if project.is_gold and project.deadline %}
                            <div class="text-muted mb-2" style="font-size: 0.8rem;">
                                <i class="bi bi-clock me-1"></i>
                                Deadline: {{ project.deadline|date:"M d, Y" }}
                            </div>
                            {% endif %}

                            <p class="card-text small text-muted mb-2" style="font-size: 0.85rem;">
                                {{ project.description|truncatechars:100 }}
                            </p>

                            {% if project.tags %}
                            <div class="mb-2">
                                {% for tag in project.tag_list|slice:":3" %}
                                <a href="?tags={{ tag }}" 
                                   class="badge bg-light text-dark text-decoration-none me-1"
                                   style="font-size: 0.75rem;">
                                    {{ tag }}
                                </a>
                                {% endfor %}
                            </div>
                            {% endif %}
                        </div>

                        <div class="card-footer bg-transparent py-2">
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="d-flex align-items-center">
                                    <img src="{% if project.author.profile.avatar %}{{ project.author.profile.avatar.url }}{% else %}{% static 'images/default-avatar.png' %}{% endif %}" 
                                         class="rounded-circle me-2" 
                                         alt="{{ project.author.username }}"
                                         style="width: 24px; height: 24px; object-fit: cover;">
                                    <div style="font-size: 0.85rem;">
                                        <a href="{% url 'projects:user_profile' username=project.author.username %}" 
                                           class="text-decoration-none text-dark">
                                            {{ project.author.get_full_name|default:project.author.username|truncatechars:15 }}
                                        </a>
                                        {% if project.author.profile.is_faculty %}
                                        <span class="badge bg-primary" style="font-size: 0.7rem;">Faculty</span>
                                        {% endif %}
                                    </div>
                                </div>
                                <div class="project-stats" style="font-size: 0.75rem;">
                                    <span class="text-muted me-2" title="Claps">
                                        <i class="bi bi-hand-thumbs-up"></i> {{ project.clap_count }}
                                    </span>
                                    <span class="text-muted" title="Comments">
                                        <i class="bi bi-chat"></i> {{ project.comment_count }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                {% empty %}
                <div class="col-12">
                    <div class="alert alert-info text-center">
                        No projects found matching your criteria.
                    </div>
                </div>
                {% endfor %}
            </div>

            <!-- Pagination -->
            {% if page_obj.has_other_pages %}
            <div class="mt-4">
                {% include "includes/pagination.html" with page_obj=page_obj %}
            </div>
            {% endif %}
        </div>
    </div>
</div>

<style>
.project-card {
    transition: transform 0.2s ease-in-out;
}

.project-card:hover {
    transform: translateY(-5px);
}

.project-card .card-title {
    font-size: 1rem;
    line-height: 1.4;
}

.project-card .badge {
    font-weight: normal;
}

.card-badges {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    z-index: 2;
}

/* Reduce spacing in card body */
.project-card .card-body {
    padding: 1rem;
}

.project-card .card-footer {
    padding: 0.5rem 1rem;
    border-top: 1px solid rgba(0,0,0,.075);
}

/* Make tags more compact */
.project-card .badge {
    padding: 0.35em 0.65em;
}

/* Improve accessibility */
@media (hover: hover) {
    .project-card a:hover {
        text-decoration: underline !important;
    }
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .project-card .card-title {
        font-size: 0.95rem;
    }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Auto-submit form when radio buttons change
    const categoryRadios = document.querySelectorAll('input[name="category"]');
    categoryRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            document.getElementById('filterForm').submit();
        });
    });

    // Handle sort select change
    const sortSelect = document.querySelector('select[name="sort"]');
    sortSelect.addEventListener('change', () => {
        document.getElementById('filterForm').submit();
    });

    // Preserve scroll position after form submit
    const scrollPosition = sessionStorage.getItem('scrollPosition');
    if (scrollPosition) {
        window.scrollTo(0, parseInt(scrollPosition));
        sessionStorage.removeItem('scrollPosition');
    }

    window.addEventListener('beforeunload', () => {
        sessionStorage.setItem('scrollPosition', window.scrollY.toString());
    });
});
</script>
{% endblock %}

# Contents from: .\projects\project_solution.html
{% extends 'base.html' %}
{% load static %}
{% load project_tags %}

{% block content %}
<div class="container py-4">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h2 class="mb-1">Solutions for {{ project.title }}</h2>
            <p class="text-muted mb-0">
                <i class="bi bi-file-earmark-text me-2"></i>
                {{ solutions|length }} submission{{ solutions|length|pluralize:",s" }}
            </p>
        </div>
        <a href="{% url 'projects:project_detail' project.pk %}" class="btn btn-outline-primary">
            <i class="bi bi-arrow-left me-2"></i>Back to Project
        </a>
    </div>

    <!-- Solutions List -->
    {% if solutions %}
        <div class="card shadow-sm">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead>
                        <tr>
                            <th>Student</th>
                            <th>Submitted</th>
                            <th>Status</th>
                            <th>GitHub</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for solution in solutions %}
                            <tr>
                                <td>
                                    <div class="d-flex align-items-center">
                                        {% if solution.user.profile.avatar %}
                                            <img src="{{ solution.user.profile.avatar.url }}" 
                                                 class="rounded-circle me-2" 
                                                 width="32" height="32"
                                                 alt="{{ solution.user.get_full_name }}">
                                        {% endif %}
                                        <div>
                                            <div>{{ solution.user.get_full_name|default:solution.user.username }}</div>
                                            <small class="text-muted">@{{ solution.user.username }}</small>
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    <div>{{ solution.created_at|date:"M d, Y" }}</div>
                                    <small class="text-muted">{{ solution.created_at|time:"H:i" }}</small>
                                </td>
                                <td>
                                    {% if solution.is_approved %}
                                        <span class="badge bg-success">
                                            <i class="bi bi-check-circle me-1"></i>Approved
                                        </span>
                                    {% elif solution.faculty_feedback %}
                                        <span class="badge bg-warning">
                                            <i class="bi bi-exclamation-circle me-1"></i>Needs Revision
                                        </span>
                                    {% else %}
                                        <span class="badge bg-secondary">
                                            <i class="bi bi-clock me-1"></i>Pending Review
                                        </span>
                                    {% endif %}
                                </td>
                                <td>
                                    {% if solution.github_link %}
                                        <a href="{{ solution.github_link }}" 
                                           target="_blank"
                                           class="btn btn-sm btn-outline-secondary">
                                            <i class="bi bi-github me-1"></i>View Code
                                        </a>
                                    {% else %}
                                        <span class="text-muted">-</span>
                                    {% endif %}
                                </td>
                                <td>
                                    <div class="btn-group">
                                        <a href="{% url 'projects:solution_detail' solution.pk %}" 
                                           class="btn btn-sm btn-outline-primary">
                                            <i class="bi bi-eye me-1"></i>View
                                        </a>
                                        <a href="{% url 'projects:review_solution' project.pk solution.pk %}" 
                                           class="btn btn-sm btn-primary">
                                            <i class="bi bi-pencil me-1"></i>Review
                                        </a>
                                    </div>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    {% else %}
        <div class="card shadow-sm">
            <div class="card-body text-center py-5">
                <i class="bi bi-inbox display-1 text-muted mb-3"></i>
                <h3>No Solutions Yet</h3>
                <p class="text-muted mb-0">There are no solutions submitted for this project yet.</p>
            </div>
        </div>
    {% endif %}
</div>
{% endblock %}

# Contents from: .\projects\rating_model.html
<!-- templates/projects/includes/rating_modal.html -->
<div class="modal fade" id="ratingModal" tabindex="-1" aria-labelledby="ratingModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="ratingModalLabel">Rate this project</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form id="ratingForm" method="post" action="{% url 'projects:rate_project' project.pk %}">
                <div class="modal-body">
                    {% csrf_token %}
                    <div class="rating-stars text-center mb-3">
                        <div class="stars">
                            {% for i in "12345" %}
                            <i class="bi bi-star star-rating" data-rating="{{ forloop.counter }}"></i>
                            {% endfor %}
                        </div>
                        <input type="hidden" name="score" id="selected-rating" value="">
                    </div>
                    <div class="mb-3">
                        <label for="review" class="form-label">Review (optional)</label>
                        <textarea class="form-control" id="review" name="review" rows="3"></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-light" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Submit Rating</button>
                </div>
            </form>
        </div>
    </div>
</div>

<style>
.rating-stars .stars {
    font-size: 2rem;
    color: #ffc107;
    cursor: pointer;
}

.rating-stars .stars i {
    margin: 0 2px;
}

.rating-stars .stars i.active {
    color: #ffc107;
}

.rating-stars .stars i:not(.active) {
    color: #e4e5e9;
}

.rating-stars .stars i:hover,
.rating-stars .stars i:hover ~ i {
    color: #ffc107;
}
</style>

<script>
$(document).ready(function() {
    // Handle star rating selection
    $('.star-rating').hover(
        function() {
            var rating = $(this).data('rating');
            highlightStars(rating);
        },
        function() {
            var selectedRating = $('#selected-rating').val();
            highlightStars(selectedRating);
        }
    );

    $('.star-rating').click(function() {
        var rating = $(this).data('rating');
        $('#selected-rating').val(rating);
        highlightStars(rating);
    });

    function highlightStars(rating) {
        $('.star-rating').each(function() {
            var starRating = $(this).data('rating');
            $(this).toggleClass('active', starRating <= rating);
        });
    }

    // Handle form submission
    $('#ratingForm').on('submit', function(e) {
        e.preventDefault();
        
        if (!$('#selected-rating').val()) {
            alert('Please select a rating');
            return;
        }

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.status === 'success') {
                    // Update the rating display
                    const stars = $('.project-rating .stars i');
                    stars.removeClass('bi-star-fill').addClass('bi-star');
                    stars.slice(0, Math.floor(response.rating)).removeClass('bi-star').addClass('bi-star-fill');
                    
                    // Update the rating text
                    $('.project-rating span').text(
                        `${response.rating.toFixed(1)} (${response.total_ratings} rating${response.total_ratings !== 1 ? 's' : ''})`
                    );
                    
                    // Close modal and show toast
                    $('#ratingModal').modal('hide');
                    const toast = new bootstrap.Toast($('#ratingToast'));
                    $('#ratingMessage').text('Thank you for your rating!');
                    toast.show();
                }
            },
            error: function() {
                alert('Error submitting rating. Please try again.');
            }
        });
    });
});
</script>

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
                                            <td>{{ weekly_stats.clap_count }}</td>
                                            <td>{{ monthly_stats.clap_count }}</td>
                                            <td>
                                                {% if weekly_stats.clap_count > monthly_stats.clap_count %}
                                                <span class="text-success">
                                                    <i class="bi bi-arrow-up"></i>
                                                    {{ weekly_stats.clap_count|percentage:monthly_stats.clap_count }}%
                                                </span>
                                                {% else %}
                                                <span class="text-danger">
                                                    <i class="bi bi-arrow-down"></i>
                                                    {{ monthly_stats.clap_count|percentage:weekly_stats.clap_count }}%
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

# Contents from: .\projects\review_solution.html
{% extends 'base.html' %}

{% block content %}
<div class="container py-5">
    <h2>Review Solution</h2>
    <div class="card mb-4">
        <div class="card-body">
            <h5>Solution by {{ solution.user.username }}</h5>
            <p class="text-muted">Submitted: {{ solution.submitted_at|date:"F d, Y H:i" }}</p>
            
            <div class="mb-3">
                <h6>Content:</h6>
                {{ solution.content|linebreaks }}
            </div>
            
            {% if solution.files %}
                <div class="mb-3">
                    <h6>Files:</h6>
                    <a href="{{ solution.files.url }}" class="btn btn-sm btn-outline-primary">
                        Download Files
                    </a>
                </div>
            {% endif %}
            
            {% if solution.github_link %}
                <div class="mb-3">
                    <h6>GitHub Link:</h6>
                    <a href="{{ solution.github_link }}" target="_blank">{{ solution.github_link }}</a>
                </div>
            {% endif %}
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="mb-3">
            <label class="form-label">Feedback:</label>
            <textarea name="feedback" class="form-control" rows="4">{{ solution.faculty_feedback }}</textarea>
        </div>
        
        {% if project.token_reward %}
        <div class="mb-3">
            <label class="form-label">Tokens to Award (max {{ project.token_reward }}):</label>
            <input type="number" name="tokens" class="form-control" 
                   max="{{ project.token_reward }}" value="{{ solution.tokens_awarded|default:0 }}">
        </div>
        {% endif %}
        
        <div class="mb-3">
            <div class="form-check">
                <input type="checkbox" name="is_approved" class="form-check-input" 
                       {% if solution.is_approved %}checked{% endif %}>
                <label class="form-check-label">Approve Solution</label>
            </div>
        </div>
        
        <button type="submit" class="btn btn-primary">Submit Review</button>
    </form>
</div>
{% endblock %}

# Contents from: .\projects\search.html
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
                            {{ project.clap_count }}
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
                    

# Contents from: .\projects\social_sharing.html
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

# Contents from: .\projects\solution_submitted.html
{% extends 'base.html' %}

{% block content %}
<div class="bg-success text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">
            <i class="bi bi-check-circle-fill me-2"></i>
            Solution Submitted Successfully!
        </h1>
    </div>
</div>

<div class="container py-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="card-title mb-4">
                        <i class="bi bi-info-circle-fill text-primary me-2"></i>
                        What's Next?
                    </h5>
                    
                    <div class="mb-4">
                        <p>Your solution for <strong>{{ project.title }}</strong> has been submitted successfully.</p>
                        {% if project.gold_goal %}
                            <div class="alert alert-warning">
                                <i class="bi bi-trophy-fill me-2"></i>
                                {% if project.gold_goal == 'all' %}
                                    You'll receive your tokens once your solution is verified.
                                {% elif project.gold_goal == 'first' %}
                                    If you're the first to submit a correct solution, you'll receive the tokens!
                                {% else %}
                                    The best solution will be selected to receive the tokens.
                                {% endif %}
                            </div>
                        {% endif %}
                    </div>

                    <div class="d-grid gap-2">
                        <a href="{% url 'projects:project_detail' project.pk %}" class="btn btn-primary">
                            <i class="bi bi-arrow-left me-2"></i>Back to Project
                        </a>
                        <a href="{% url 'projects:solution_detail' solution.pk %}" class="btn btn-outline-primary">
                            <i class="bi bi-eye me-2"></i>View Your Solution
                        </a>
                        <a href="{% url 'projects:project_list' %}" class="btn btn-outline-secondary">
                            <i class="bi bi-grid me-2"></i>Browse More Projects
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\projects\sponsorship_form.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<!-- Application Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">
            {% if request.GET.type == 'sponsor' %}
                Sponsorship Application
            {% else %}
                Join Our Team
            {% endif %}
        </h1>
        <p class="lead">
            {% if request.GET.type == 'sponsor' %}
                Partner with us to advance AI in healthcare
            {% else %}
                Be part of our innovative research community
            {% endif %}
        </p>
    </div>
</div>

<!-- Application Form Section -->
<section class="application-form mb-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="card shadow-sm">
                    <div class="card-body p-4">
                        <form method="post" enctype="multipart/form-data">
                            {% csrf_token %}
                            
                            <!-- Organization/Personal Details -->
                            <div class="mb-4">
                                <label class="form-label fw-bold">Name</label>
                                {{ form.name }}
                                {% if form.name.errors %}
                                    <div class="text-danger small">{{ form.name.errors }}</div>
                                {% endif %}
                            </div>
                            
                            <div class="mb-4">
                                <label class="form-label fw-bold">Email</label>
                                {{ form.email }}
                                {% if form.email.errors %}
                                    <div class="text-danger small">{{ form.email.errors }}</div>
                                {% endif %}
                            </div>
                            
                            {% if request.GET.type == 'sponsor' %}
                                <div class="mb-4">
                                    <label class="form-label fw-bold">Organization</label>
                                    {{ form.organization }}
                                </div>
                                
                                <div class="mb-4">
                                    <label class="form-label fw-bold">Sponsorship Level Interest</label>
                                    {{ form.level }}
                                    <div class="form-text text-muted">
                                        Select your preferred sponsorship tier
                                    </div>
                                </div>
                            {% endif %}
                            
                            <!-- Message/Proposal -->
                            <div class="mb-4">
                                <label class="form-label fw-bold">
                                    {% if request.GET.type == 'sponsor' %}
                                        Proposal
                                    {% else %}
                                        Message
                                    {% endif %}
                                </label>
                                {{ form.message }}
                                <div class="form-text text-muted">
                                    {% if request.GET.type == 'sponsor' %}
                                        Tell us about your organization and how you'd like to collaborate
                                    {% else %}
                                        Tell us about your background and interest in joining our team
                                    {% endif %}
                                </div>
                            </div>
                            
                            <!-- Attachments -->
                            <div class="mb-4">
                                <label class="form-label fw-bold">
                                    {% if request.GET.type == 'sponsor' %}
                                        Supporting Documents
                                    {% else %}
                                        Resume/CV
                                    {% endif %}
                                </label>
                                {{ form.attachment }}
                                <div class="form-text text-muted">
                                    PDF format preferred, max 10MB
                                </div>
                            </div>
                            
                            <!-- Submit Buttons -->
                            <div class="d-flex justify-content-center gap-3 mt-5">
                                <button type="submit" class="btn btn-primary px-4">
                                    Submit Application
                                </button>
                                <a href="{% url 'projects:home' %}" 
                                   class="btn btn-outline-secondary px-4">
                                    Cancel
                                </a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Contact Section -->
<section class="contact-us bg-light py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Questions?</h2>
                <p class="mb-4">
                    If you have any questions about the application process,
                    please don't hesitate to reach out.
                </p>
                <div class="d-flex justify-content-center gap-3">
                    <a href="mailto:contact@example.com" class="btn btn-outline-primary">
                        <i class="bi bi-envelope me-2"></i>Contact Us
                    </a>
                    <a href="{% url 'projects:faq' %}" class="btn btn-primary">
                        <i class="bi bi-question-circle me-2"></i>View FAQs
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}

# Contents from: .\projects\sponsorship_list.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<!-- Sponsors Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Our Sponsors</h1>
        <p class="lead">Thank you to our valued sponsors who make our work possible</p>
    </div>
</div>

<!-- Sponsors Section -->
<section class="sponsors mb-5">
    <div class="container">
        <!-- Platinum Sponsors -->
        {% if sponsorships.platinum %}
        <h2 class="h3 text-center mb-5">Platinum Sponsors</h2>
        <div class="row g-4">
            {% for sponsor in sponsorships.platinum %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <img src="{{ sponsor.logo.url }}" 
                             alt="{{ sponsor.name }}" 
                             class="mb-3" 
                             style="width: 150px; height: 150px; object-fit: contain;">
                        <h3 class="h5 mb-2">{{ sponsor.name }}</h3>
                        <p class="text-muted small mb-3">{{ sponsor.description|truncatewords:30 }}</p>
                        <div class="d-flex justify-content-center gap-2">
                            <a href="{{ sponsor.website }}" class="btn btn-sm btn-outline-primary" target="_blank">
                                <i class="bi bi-box-arrow-up-right me-1"></i>Visit Website
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        <!-- Gold Sponsors -->
        {% if sponsorships.gold %}
        <h2 class="h3 text-center mb-5">Gold Sponsors</h2>
        <div class="row g-4">
            {% for sponsor in sponsorships.gold %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <img src="{{ sponsor.logo.url }}" 
                             alt="{{ sponsor.name }}" 
                             class="mb-3" 
                             style="width: 150px; height: 150px; object-fit: contain;">
                        <h3 class="h5 mb-2">{{ sponsor.name }}</h3>
                        <p class="text-muted small mb-3">{{ sponsor.description|truncatewords:30 }}</p>
                        <div class="d-flex justify-content-center gap-2">
                            <a href="{{ sponsor.website }}" class="btn btn-sm btn-outline-primary" target="_blank">
                                <i class="bi bi-box-arrow-up-right me-1"></i>Visit Website
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        <!-- Silver Sponsors -->
        {% if sponsorships.silver %}
        <h2 class="h3 text-center mb-5">Silver Sponsors</h2>
        <div class="row g-4">
            {% for sponsor in sponsorships.silver %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <img src="{{ sponsor.logo.url }}" 
                             alt="{{ sponsor.name }}" 
                             class="mb-3" 
                             style="width: 150px; height: 150px; object-fit: contain;">
                        <h3 class="h5 mb-2">{{ sponsor.name }}</h3>
                        <p class="text-muted small mb-3">{{ sponsor.description|truncatewords:30 }}</p>
                        <div class="d-flex justify-content-center gap-2">
                            <a href="{{ sponsor.website }}" class="btn btn-sm btn-outline-primary" target="_blank">
                                <i class="bi bi-box-arrow-up-right me-1"></i>Visit Website
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        <!-- Bronze Sponsors -->
        {% if sponsorships.bronze %}
        <h2 class="h3 text-center mb-5">Bronze Sponsors</h2>
        <div class="row g-4">
            {% for sponsor in sponsorships.bronze %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <img src="{{ sponsor.logo.url }}" 
                             alt="{{ sponsor.name }}" 
                             class="mb-3" 
                             style="width: 150px; height: 150px; object-fit: contain;">
                        <h3 class="h5 mb-2">{{ sponsor.name }}</h3>
                        <p class="text-muted small mb-3">{{ sponsor.description|truncatewords:30 }}</p>
                        <div class="d-flex justify-content-center gap-2">
                            <a href="{{ sponsor.website }}" class="btn btn-sm btn-outline-primary" target="_blank">
                                <i class="bi bi-box-arrow-up-right me-1"></i>Visit Website
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</section>

<!-- Contact Section -->
<section class="contact-us bg-light py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Become a Sponsor</h2>
                <p class="mb-4">
                    Interested in supporting AI research in healthcare? 
                    Join us in making a difference.
                </p>
                <div class="d-flex justify-content-center gap-3">
                    <a href="mailto:sponsorship@example.com" class="btn btn-outline-primary">
                        <i class="bi bi-envelope me-2"></i>Contact Us
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}

# Contents from: .\projects\startup_list.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<!-- Startups Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Our Startups</h1>
        <p class="lead">Discover innovative startups from our community</p>
    </div>
</div>

<!-- Featured Startups Section -->
<section class="featured-startups mb-5">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-5">
            <h2 class="h3 text-center">Featured Startups</h2>
            {% if user.is_authenticated %}
            <a href="{% url 'projects:create_startup' %}" class="btn btn-primary">
                <i class="bi bi-plus-circle me-2"></i>Add Startup
            </a>
            {% endif %}
        </div>
        
        <div class="row g-4">
            {% for startup in startups %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <img src="{{ startup.logo.url|default:'https://via.placeholder.com/150' }}" 
                             alt="{{ startup.name }}" 
                             class="rounded-circle mb-3" 
                             style="width: 150px; height: 150px; object-fit: cover;">
                        <h3 class="h5 mb-2">{{ startup.name }}</h3>
                        <p class="text-primary small mb-2">Founded by {{ startup.founder.get_full_name }}</p>
                        <p class="text-muted small mb-3">{{ startup.description|truncatewords:30 }}</p>
                        <div class="d-flex justify-content-center gap-2">
                            {% if startup.website %}
                            <a href="{{ startup.website }}" class="text-dark" target="_blank">
                                <i class="bi bi-globe"></i>
                            </a>
                            {% endif %}
                            {% if startup.linkedin_url %}
                            <a href="{{ startup.linkedin_url }}" class="text-dark" target="_blank">
                                <i class="bi bi-linkedin"></i>
                            </a>
                            {% endif %}
                            {% if startup.email %}
                            <a href="mailto:{{ startup.email }}" class="text-dark">
                                <i class="bi bi-envelope"></i>
                            </a>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="col-12 text-center">
                <p class="text-muted">No startups have been added yet.</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Contact Section -->
<section class="contact-us bg-light py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Contact Us</h2>
                <p class="mb-4">
                    Interested in learning more about our startup community or want to get involved? 
                    We'd love to hear from you.
                </p>
                <div class="d-flex justify-content-center gap-3">
                    <a href="mailto:startups@example.com" class="btn btn-outline-primary">
                        <i class="bi bi-envelope me-2"></i>Email Us
                    </a>
                    <a href="{% url 'projects:apply' %}?type=startup" class="btn btn-primary">
                        <i class="bi bi-rocket me-2"></i>Join Our Community
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Join Us Section -->
<section class="join-us bg-light py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Launch Your Startup</h2>
                <p class="mb-4">
                    Ready to take your startup to the next level? Join our thriving community of innovators
                    and entrepreneurs. Get access to resources, mentorship, and networking opportunities.
                </p>
                <a href="{% url 'projects:apply' %}?type=startup" class="btn btn-primary">
                    <i class="bi bi-rocket me-2"></i>Apply Now
                </a>
            </div>
        </div>
    </div>
</section>
{% endblock %}

# Contents from: .\projects\startups\startup_form.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<!-- Startup Form Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">
            {% if form.instance.pk %}
                Edit Startup
            {% else %}
                Add New Startup
            {% endif %}
        </h1>
        <p class="lead">Share your startup's story with our community</p>
    </div>
</div>

<div class="container my-5">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card shadow-sm">
                <div class="card-body p-4">
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <!-- Logo Upload Section -->
                        <div class="text-center mb-4">
                            {% if form.instance.logo %}
                                <img src="{{ form.instance.logo.url }}" 
                                     alt="Current logo" 
                                     class="rounded-circle mb-3"
                                     style="width: 150px; height: 150px; object-fit: cover;">
                            {% endif %}
                            <div class="mb-3">
                                {{ form.logo }}
                                <div class="form-text">Upload a square logo (recommended size: 500x500px)</div>
                            </div>
                        </div>

                        <!-- Startup Details -->
                        <div class="mb-4">
                            <label class="form-label fw-bold">Startup Name</label>
                            {{ form.name }}
                            {% if form.name.errors %}
                                <div class="invalid-feedback">{{ form.name.errors }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-bold">Description</label>
                            {{ form.description }}
                            <div class="form-text">Tell us about your startup's mission and vision</div>
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-bold">Website</label>
                            {{ form.website }}
                            <div class="form-text">Share your startup's online presence</div>
                        </div>

                        <!-- Action Buttons -->
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">
                                {% if form.instance.pk %}
                                    Update Startup
                                {% else %}
                                    Add Startup
                                {% endif %}
                            </button>
                            <a href="{% url 'projects:startup_list' %}" class="btn btn-outline-secondary">
                                <i class="bi bi-arrow-left me-2"></i>Back to Startups
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\projects\submit_project.html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<!-- Project Submission Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">{{ title }}</h1>
        <p class="lead">Share your seed with the community</p>
        {% if 'Faculty' in user.groups.all|stringformat:'s' %}
        <div class="mt-3">
            <span class="badge bg-warning text-dark">
                <i class="bi bi-star-fill me-2"></i>Faculty Member
            </span>
            <span class="ms-2 text-light">
                <i class="bi bi-info-circle me-1"></i>
                You can create Gold Seed projects with token rewards
            </span>
        </div>
        {% endif %}
    </div>
</div>

<div class="container">
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        
        <div class="row">
            <div class="col-md-8">
                <!-- Basic Project Info -->
                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3">
                            <i class="bi bi-info-circle-fill text-primary me-2"></i>
                            Project Information
                        </h5>
                        {{ form.title|as_crispy_field }}
                        {{ form.description|as_crispy_field }}
                        {{ form.tags|as_crispy_field }}
                    </div>
                </div>
                
                <!-- Links -->
                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3">
                            <i class="bi bi-link-45deg text-primary me-2"></i>
                            Links
                        </h5>
                        {{ form.github_link|as_crispy_field }}
                        {{ form.youtube_url|as_crispy_field }}
                    </div>
                </div>
                
                <!-- Files -->
                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3">
                            <i class="bi bi-file-earmark-text text-primary me-2"></i>
                            Files
                        </h5>
                        {{ form.featured_image|as_crispy_field }}
                        {{ form.pdf_file|as_crispy_field }}
                        {{ form.additional_files|as_crispy_field }}
                    </div>
                </div>
                
                {% if 'Faculty' in user.groups.all|stringformat:'s' %}
                <!-- Gold Seed Settings (Faculty Only) -->
                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3">
                            <i class="bi bi-trophy-fill text-warning me-2"></i>
                            Gold Seed Settings
                        </h5>
                        <div class="form-check mb-3">
                            {{ form.is_gold }}
                            <label class="form-check-label" for="{{ form.is_gold.id_for_label }}">
                                Make this a Gold Seed
                            </label>
                            {% if form.is_gold.help_text %}
                                <small class="form-text text-muted d-block mt-1">{{ form.is_gold.help_text }}</small>
                            {% endif %}
                        </div>
                        
                        <div class="gold-seed-options" style="display: none;">
                            {{ form.token_reward|as_crispy_field }}
                            {{ form.gold_goal|as_crispy_field }}
                            {{ form.deadline|as_crispy_field }}
                        </div>
                    </div>
                </div>
                {% endif %}
                
                <div class="card shadow-sm">
                    <div class="card-body">
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-cloud-upload me-2"></i>Submit Seed
                            </button>
                            <a href="{% url 'projects:project_list' %}" class="btn btn-outline-secondary">
                                <i class="bi bi-arrow-left me-2"></i>Back to Projects
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <!-- Submission Guidelines -->
                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h5 class="card-title">
                            <i class="bi bi-lightbulb-fill text-warning me-2"></i>
                            Submission Tips
                        </h5>
                        <ul class="list-unstyled mb-0">
                            <li class="mb-2"><i class="bi bi-check-circle text-success me-2"></i>Provide a clear, detailed description</li>
                            <li class="mb-2"><i class="bi bi-check-circle text-success me-2"></i>Include relevant code samples</li>
                            <li class="mb-2"><i class="bi bi-check-circle text-success me-2"></i>Add meaningful tags for better discovery</li>
                            <li><i class="bi bi-check-circle text-success me-2"></i>Share your GitHub repository if available</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </form>
</div>

{% if 'Faculty' in user.groups.all|stringformat:'s' %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const isGoldCheckbox = document.getElementById('{{ form.is_gold.id_for_label }}');
    const goldOptions = document.querySelector('.gold-seed-options');
    
    function toggleGoldOptions() {
        goldOptions.style.display = isGoldCheckbox.checked ? 'block' : 'none';
    }
    
    isGoldCheckbox.addEventListener('change', toggleGoldOptions);
    toggleGoldOptions(); // Initial state
});
</script>
{% endif %}
{% endblock %}

# Contents from: .\projects\submit_solution.html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<!-- Solution Header Banner -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Submit Solution</h1>
        <p class="lead">{{ project.title }}</p>
        {% if project.deadline %}
            <div class="d-flex align-items-center mt-3">
                <i class="bi bi-clock-fill me-2"></i>
                <span>Deadline: {{ project.deadline|date:"F d, Y H:i" }}</span>
            </div>
        {% endif %}
        {% if project.token_reward %}
            <div class="d-flex align-items-center mt-2">
                <i class="bi bi-coin me-2"></i>
                <span>Reward: {{ project.token_reward }} Tokens</span>
            </div>
        {% endif %}
    </div>
</div>

<div class="container py-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <!-- Project Details Card -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <h5 class="card-title mb-3">
                        <i class="bi bi-info-circle-fill text-primary me-2"></i>
                        Project Details
                    </h5>
                    <p class="card-text">{{ project.description }}</p>
                    {% if project.github_link %}
                        <a href="{{ project.github_link }}" target="_blank" class="btn btn-outline-secondary btn-sm">
                            <i class="bi bi-github me-2"></i>View Project Repository
                        </a>
                    {% endif %}
                </div>
            </div>

            <!-- Solution Form Card -->
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="card-title mb-4">
                        <i class="bi bi-send-fill text-primary me-2"></i>
                        Submit Your Solution
                    </h5>
                    
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <!-- Solution Content -->
                        <div class="mb-4">
                            {{ form.content|as_crispy_field }}
                        </div>
                        
                        <!-- GitHub Link -->
                        <div class="mb-4">
                            {{ form.github_link|as_crispy_field }}
                        </div>
                        
                        <!-- Files -->
                        <div class="mb-4">
                            {{ form.files|as_crispy_field }}
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-send me-2"></i>Submit Solution
                            </button>
                            <a href="{% url 'projects:project_detail' project.pk %}" 
                               class="btn btn-outline-secondary">
                                <i class="bi bi-arrow-left me-2"></i>Back to Project
                            </a>
                        </div>
                    </form>
                </div>
            </div>
            
            {% if project.gold_goal %}
            <!-- Submission Guidelines -->
            <div class="card shadow-sm mt-4">
                <div class="card-body">
                    <h5 class="card-title text-warning mb-3">
                        <i class="bi bi-trophy-fill me-2"></i>
                        Gold Seed Challenge
                    </h5>
                    <p class="mb-0">
                        <strong>Goal Type:</strong>
                        {% if project.gold_goal == 'all' %}
                            All participants who complete this challenge will receive tokens
                        {% elif project.gold_goal == 'first' %}
                            First participant to complete this challenge will receive tokens
                        {% else %}
                            Best solution will receive tokens
                        {% endif %}
                    </p>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\projects\talents.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<!-- Talents Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Our Talents</h1>
        <p class="lead">Discover our community of talented developers and their amazing projects</p>
    </div>
</div>

<div class="container py-5">
    <!-- Talent Type Filter -->
    <div class="text-center mb-5">
        <div class="d-flex justify-content-center gap-2 mt-4">
            <a href="{% url 'projects:talents' %}" 
               class="btn btn-{% if not selected_talent %}primary{% else %}outline-primary{% endif %} btn-sm">
                All
            </a>
            {% for value, label in talent_types %}
                <a href="{% url 'projects:talents' %}?talent_type={{ value }}" 
                   class="btn btn-{% if selected_talent == value %}primary{% else %}outline-primary{% endif %} btn-sm">
                    {{ label }}
                </a>
            {% endfor %}
        </div>
    </div>

    <!-- Talents Grid -->
    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        {% for talent in talents %}
        <div class="col">
            <div class="card h-100 shadow-sm hover-card">
                <div class="card-body text-center">
                    <!-- Avatar -->
                    <img src="{% if talent.profile.avatar %}{{ talent.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ talent.username }}{% endif %}" 
                         alt="{{ talent.username }}" 
                         class="rounded-circle mb-3"
                         style="width: 100px; height: 100px; object-fit: cover;">
                    
                    <!-- Name and Username -->
                    <h5 class="card-title mb-1">
                        {{ talent.get_full_name|default:talent.username }}
                    </h5>
                    <p class="text-muted small mb-2">@{{ talent.username }}</p>
                    
                    <!-- Talent Type -->
                    {% if talent.profile.talent_type %}
                        <span class="badge bg-primary mb-3">
                            {{ talent.profile.get_talent_display }}
                        </span>
                    {% endif %}
                    
                    <!-- Bio -->
                    {% if talent.profile.bio %}
                    <p class="card-text small mb-3">
                        {{ talent.profile.bio|truncatechars:100 }}
                    </p>
                    {% endif %}
                    
                    <!-- Stats -->
                    <div class="d-flex justify-content-center gap-3 mb-3">
                        <div class="text-center">
                            <h6 class="mb-0">{{ talent.project_count }}</h6>
                            <small class="text-muted">Projects</small>
                        </div>
                        <div class="text-center">
                            <h6 class="mb-0">{{ talent.follower_count }}</h6>
                            <small class="text-muted">Followers</small>
                        </div>
                        <div class="text-center">
                            <h6 class="mb-0">{{ talent.following_count }}</h6>
                            <small class="text-muted">Following</small>
                        </div>
                    </div>
                    
                    <!-- Social Links -->
                    <div class="d-flex justify-content-center gap-2 mb-3">
                        {% if talent.profile.github_username %}
                        <a href="https://github.com/{{ talent.profile.github_username }}" 
                           class="btn btn-sm btn-outline-dark" 
                           target="_blank">
                            <i class="bi bi-github"></i>
                        </a>
                        {% endif %}
                        
                        {% if talent.profile.twitter_username %}
                        <a href="https://twitter.com/{{ talent.profile.twitter_username }}" 
                           class="btn btn-sm btn-outline-primary" 
                           target="_blank">
                            <i class="bi bi-twitter"></i>
                        </a>
                        {% endif %}
                        
                        {% if talent.profile.website %}
                        <a href="{{ talent.profile.website }}" 
                           class="btn btn-sm btn-outline-secondary" 
                           target="_blank">
                            <i class="bi bi-globe"></i>
                        </a>
                        {% endif %}
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="d-flex justify-content-center gap-2">
                        <a href="{% url 'projects:user_profile' talent.username %}" 
                           class="btn btn-primary">
                            View Profile
                        </a>
                        {% if user.is_authenticated and user != talent %}
                            <button class="btn btn-outline-primary follow-btn" 
                                    data-username="{{ talent.username }}"
                                    {% if user in talent.followers.all %}data-following="true"{% endif %}>
                                {% if user in talent.followers.all %}
                                    Unfollow
                                {% else %}
                                    Follow
                                {% endif %}
                            </button>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12 text-center">
            <p class="text-muted">No talents found</p>
        </div>
        {% endfor %}
    </div>
</div>

<!-- JavaScript for Follow Button -->
{% block extra_js %}
<script>
$(document).ready(function() {
    $('.follow-btn').click(function() {
        const btn = $(this);
        const username = btn.data('username');
        const isFollowing = btn.data('following');
        const url = isFollowing 
            ? "{% url 'projects:unfollow_user' 'username' %}"
            : "{% url 'projects:follow_user' 'username' %}";
        
        $.post(url.replace('username', username), {
            csrfmiddlewaretoken: '{{ csrf_token }}'
        })
        .done(function(response) {
            btn.data('following', !isFollowing);
            btn.text(isFollowing ? 'Follow' : 'Unfollow');
            location.reload(); // Refresh to update counts
        })
        .fail(function() {
            alert('Error updating follow status');
        });
    });
});
</script>
{% endblock %}
{% endblock content %}

# Contents from: .\projects\tool_form.html
<!-- templates/projects/tools/tool_form.html -->
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow">
                <div class="card-body">
                    <h2 class="card-title text-center mb-4">
                        {% if form.instance.pk %}
                            Edit Tool
                        {% else %}
                            Add New Tool
                        {% endif %}
                    </h2>
                    
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label class="form-label">Tool Name</label>
                            {{ form.name }}
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Description</label>
                            {{ form.description }}
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Screenshot/Demo Image</label>
                            {% if form.instance.image %}
                                <div class="mb-2">
                                    <img src="{{ form.instance.image.url }}" alt="Current image" 
                                         style="max-height: 200px;">
                                </div>
                            {% endif %}
                            {{ form.image }}
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Tool URL</label>
                            {{ form.url }}
                            <div class="form-text">Link to the live tool or demo</div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">GitHub Repository</label>
                            {{ form.github_url }}
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Documentation URL</label>
                            {{ form.documentation_url }}
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">
                                {% if form.instance.pk %}
                                    Update Tool
                                {% else %}
                                    Add Tool
                                {% endif %}
                            </button>
                            <a href="{% url 'projects:tool_list' %}" class="btn btn-outline-secondary">
                                Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>


# Contents from: .\projects\tool_list.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<!-- Tools Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Our AI Tools</h1>
        <p class="lead">Explore our collection of AI tools and utilities</p>
    </div>
</div>

<!-- Tools Section -->
<section class="tools mb-5">
    <div class="container">
        <h2 class="h3 text-center mb-5">Available Tools</h2>
        
        <div class="row g-4">
            {% for tool in tools %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <img src="{{ tool.image.url }}" 
                             alt="{{ tool.name }}" 
                             class="mb-3" 
                             style="width: 150px; height: 150px; object-fit: contain;">
                        <h3 class="h5 mb-2">{{ tool.name }}</h3>
                        <p class="text-muted small mb-3">{{ tool.description|truncatewords:30 }}</p>
                        <div class="d-flex justify-content-center gap-2">
                            <a href="{{ tool.url }}" class="btn btn-sm btn-outline-primary" target="_blank">
                                <i class="bi bi-box-arrow-up-right me-1"></i>Try It
                            </a>
                            {% if tool.github_url %}
                            <a href="{{ tool.github_url }}" class="btn btn-sm btn-outline-secondary" target="_blank">
                                <i class="bi bi-github me-1"></i>GitHub
                            </a>
                            {% endif %}
                            {% if tool.documentation_url %}
                            <a href="{{ tool.documentation_url }}" class="btn btn-sm btn-outline-info" target="_blank">
                                <i class="bi bi-book me-1"></i>Docs
                            </a>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="col-12 text-center">
                <p class="text-muted">No tools have been added yet.</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Contact Section -->
<section class="contact-us bg-light py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <h2 class="h3 mb-4">Need Help?</h2>
                <p class="mb-4">
                    Have questions about our tools or need technical support? 
                    We're here to help.
                </p>
                <div class="d-flex justify-content-center gap-3">
                    <a href="mailto:support@example.com" class="btn btn-outline-primary">
                        <i class="bi bi-envelope me-2"></i>Contact Support
                    </a>
                    <a href="{% url 'projects:help' %}" class="btn btn-primary">
                        <i class="bi bi-question-circle me-2"></i>Documentation
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}

# Contents from: .\projects\user_profile.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="bg-primary py-4 mb-4"></div>
    <div class="container">
        <h1 class="text-white mb-2">{{ profile_user.get_full_name }}</h1>
        {% if profile_user.profile.title or profile_user.profile.department %}
            <p class="text-white-50 mb-0">
                {% if profile_user.profile.title %}{{ profile_user.profile.title }}{% endif %}
                {% if profile_user.profile.department %}
                    {% if profile_user.profile.title %} • {% endif %}
                    {{ profile_user.profile.department }}
                {% endif %}
            </p>
        {% endif %}
    </div>
</div>
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
                    
                    <h4 class="card-title">{{ profile_user.get_full_name }}</h4>
                    {% if profile_user.userprofile.talent_type %}
                        <span class="badge bg-primary mb-2">{{ profile_user.userprofile.get_talent_display }}</span>
                    {% endif %}
                    {% if is_faculty %}
                        <span class="badge bg-secondary mb-2">Faculty</span>
                    {% endif %}

                    {% if profile_user.profile.title %}
                        <p class="text-muted mb-1">{{ profile_user.profile.title }}</p>
                    {% endif %}
                    {% if profile_user.profile.department %}
                        <p class="text-muted mb-3">{{ profile_user.profile.department }}</p>
                    {% endif %}
                    
                    {% if profile_user.profile.bio %}
                        <p class="text-muted mb-3">{{ profile_user.profile.bio }}</p>
                    {% endif %}

                    <div class="d-flex justify-content-center gap-3 mb-3">
                        <div class="text-center">
                            <h6 class="mb-0">{{ stats.projects_count }}</h6>
                            <small class="text-muted">Seeds</small>
                        </div>
                        <div class="text-center">
                            <h6 class="mb-0">{{ stats.followers_count }}</h6>
                            <small class="text-muted">Followers</small>
                        </div>
                        <div class="text-center">
                            <h6 class="mb-0">{{ stats.following_count }}</h6>
                            <small class="text-muted">Following</small>
                        </div>
                        <div class="text-center">
                            <h6 class="mb-0">{{ stats.total_claps }}</h6>
                            <small class="text-muted">Claps</small>
                        </div>
                        <div class="text-center">
                            <h6 class="mb-0">{{ stats.total_comments }}</h6>
                            <small class="text-muted">Comments</small>
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

                    <!-- Social Links -->
                    <div class="mt-4 d-flex justify-content-center gap-3">
                        {% if profile_user.profile.github_username %}
                            <a href="https://github.com/{{ profile_user.profile.github_username }}" 
                               target="_blank"
                               class="text-dark">
                                <i class="bi bi-github fs-5"></i>
                            </a>
                        {% endif %}

                        {% if profile_user.profile.linkedin_url %}
                            <a href="{{ profile_user.profile.linkedin_url }}" 
                               target="_blank"
                               class="text-primary">
                                <i class="bi bi-linkedin fs-5"></i>
                            </a>
                        {% endif %}

                        {% if profile_user.profile.twitter_username %}
                            <a href="https://twitter.com/{{ profile_user.profile.twitter_username }}" 
                               target="_blank"
                               class="text-info">
                                <i class="bi bi-twitter fs-5"></i>
                            </a>
                        {% endif %}

                        {% if profile_user.profile.website %}
                            <a href="{{ profile_user.profile.website }}" 
                               target="_blank"
                               class="text-dark">
                                <i class="bi bi-globe fs-5"></i>
                            </a>
                        {% endif %}

                        {% if profile_user.email %}
                            <a href="mailto:{{ profile_user.email }}" class="text-dark">
                                <i class="bi bi-envelope fs-5"></i>
                            </a>
                        {% endif %}
                    </div>
                </div>
            </div>

            <!-- Additional Info Card -->
            <div class="card shadow-sm mt-4">
                <div class="card-body">
                    <h5 class="card-title mb-3">About</h5>
                    
                    {% if profile_user.profile.research_interests %}
                        <div class="mb-3">
                            <h6 class="text-muted mb-2">Research Interests</h6>
                            <p>{{ profile_user.profile.research_interests }}</p>
                        </div>
                    {% endif %}

                    {% if profile_user.profile.location %}
                        <div class="mb-3">
                            <h6 class="text-muted mb-2">Location</h6>
                            <p>{{ profile_user.profile.location }}</p>
                        </div>
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
                                <i class="bi bi-hand-thumbs-up ms-3"></i> {{ project.clap_count }}
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

# Contents from: .\projects\virtual_member_list.html
<!-- templates/projects/virtual_members/virtual_member_list.html -->
<div class="container py-5">
    <div class="row mb-4">
        <div class="col">
            <h1 class="fw-bold">Virtual Team Members</h1>
            <p class="text-muted">Meet our AI-powered virtual team members</p>
        </div>
    </div>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        {% for member in virtual_members %}
        <div class="col">
            <div class="card h-100 shadow-sm">
                <img src="{{ member.avatar.url }}" class="card-img-top rounded-circle p-3 mx-auto" alt="{{ member.name }}" style="width: 200px; height: 200px; object-fit: cover;">
                <div class="card-body text-center">
                    <h5 class="card-title">{{ member.name }}</h5>
                    <p class="card-subtitle mb-2 text-muted">
                        <p class="card-subtitle mb-2 text-muted">{{ member.specialty }}</p>
                    <p class="card-text">{{ member.description }}</p>
                </div>
                <div class="card-footer bg-transparent">
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">{{ member.projects.count }} projects</small>
                        <button class="btn btn-sm btn-outline-primary add-to-project-btn" 
                                data-member-id="{{ member.id }}">
                            <i class="bi bi-plus-circle me-1"></i>Add to Project
                        </button>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12 text-center py-5">
            <p class="text-muted">No virtual members available.</p>
        </div>
        {% endfor %}
    </div>
</div>

# Contents from: .\registration\login.html
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

# Contents from: .\registration\register.html
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

# Contents from: .\teams\create_team.html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<!-- Create Team Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Create Team</h1>
        <p class="lead">Start a new collaboration and build something amazing together</p>
    </div>
</div>

<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card shadow-sm">
                <div class="card-body">
                    <form method="post" enctype="multipart/form-data" novalidate>
                        {% csrf_token %}
                        
                        <!-- Team Information -->
                        <div class="mb-4">
                            <h5 class="card-title mb-3">
                                <i class="bi bi-info-circle-fill text-primary me-2"></i>
                                Team Information
                            </h5>
                            {{ form.name|as_crispy_field }}
                            {{ form.description|as_crispy_field }}
                        </div>
                        
                        <!-- Team Settings -->
                        <div class="mb-4">
                            <h5 class="card-title mb-3">
                                <i class="bi bi-gear-fill text-primary me-2"></i>
                                Team Settings
                            </h5>
                            {{ form.tags|as_crispy_field }}
                            {{ form.team_image|as_crispy_field }}
                            
                            {% if form.team_image.help_text %}
                            <small class="form-text text-muted">
                                {{ form.team_image.help_text }}
                            </small>
                            {% endif %}
                        </div>
                        
                        <!-- Action Buttons -->
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-plus-lg me-2"></i>Create Team
                            </button>
                            <a href="{% url 'projects:team_list' %}" class="btn btn-outline-secondary">
                                <i class="bi bi-x-lg me-2"></i>Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- Tips Card -->
            <div class="card mt-4">
                <div class="card-body">
                    <h5 class="card-title">
                        <i class="bi bi-lightbulb-fill text-warning me-2"></i>
                        Tips for Creating a Great Team
                    </h5>
                    <ul class="list-unstyled mb-0">
                        <li class="mb-2">
                            <i class="bi bi-check2 text-success me-2"></i>
                            Choose a clear, descriptive name for your team
                        </li>
                        <li class="mb-2">
                            <i class="bi bi-check2 text-success me-2"></i>
                            Write a detailed description of your team's goals
                        </li>
                        <li class="mb-2">
                            <i class="bi bi-check2 text-success me-2"></i>
                            Add relevant tags to help others find your team
                        </li>
                        <li>
                            <i class="bi bi-check2 text-success me-2"></i>
                            Upload a team image to make your team stand out
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\teams\delete_team.html
{% extends 'base.html' %}

{% block content %}
<!-- Delete Team Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Delete Team: {{ team.name }}</h1>
        <p class="lead">This action cannot be undone</p>
    </div>
</div>

<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <!-- Delete Confirmation -->
            <div class="card border-danger shadow-sm mb-4">
                <div class="card-body text-center">
                    <div class="mb-4">
                        <i class="bi bi-exclamation-triangle-fill text-danger" style="font-size: 3rem;"></i>
                    </div>
                    <h5 class="card-title text-danger">Are you sure you want to delete this team?</h5>
                    <p class="card-text mb-4">
                        This will permanently delete the team "{{ team.name }}" and all associated data. 
                        This action cannot be undone.
                    </p>
                    
                    <form method="post" class="d-inline">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-danger me-2">
                            <i class="bi bi-trash me-2"></i>Yes, Delete Team
                        </button>
                        <a href="{% url 'projects:team_detail' team_slug=team.slug %}" 
                           class="btn btn-outline-secondary">
                            <i class="bi bi-x-lg me-2"></i>Cancel
                        </a>
                    </form>
                </div>
            </div>
            
            <!-- Team Details -->
            <div class="card shadow-sm">
                <div class="card-header bg-transparent">
                    <h5 class="mb-0">Team Details</h5>
                </div>
                <div class="card-body">
                    <dl class="row mb-0">
                        <dt class="col-sm-3">Team Name</dt>
                        <dd class="col-sm-9">{{ team.name }}</dd>
                        
                        <dt class="col-sm-3">Created</dt>
                        <dd class="col-sm-9">{{ team.created_at|date:"F j, Y" }}</dd>
                        
                        <dt class="col-sm-3">Members</dt>
                        <dd class="col-sm-9">{{ team.memberships.count }}</dd>
                        
                        <dt class="col-sm-3">Founder</dt>
                        <dd class="col-sm-9">{{ team.founder.get_full_name|default:team.founder.username }}</dd>
                        
                        {% if team.description %}
                        <dt class="col-sm-3">Description</dt>
                        <dd class="col-sm-9">{{ team.description }}</dd>
                        {% endif %}
                        
                        {% if team.tags %}
                        <dt class="col-sm-3">Tags</dt>
                        <dd class="col-sm-9">
                            {% for tag in team.tags.split %}
                            <span class="badge bg-light text-dark me-1">{{ tag }}</span>
                            {% endfor %}
                        </dd>
                        {% endif %}
                    </dl>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\teams\discussion_detail.html
{% extends "base.html" %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="flex justify-between items-start mb-4">
            <div>
                <h1 class="text-2xl font-bold">{{ discussion.title }}</h1>
                <p class="text-gray-500">Posted by {{ discussion.author.username }} - {{ discussion.created_at|timesince }} ago</p>
            </div>
            <a href="{% url 'team_detail' team.slug %}" class="btn btn-secondary">Back to Team</a>
        </div>
        <div class="prose max-w-none">
            {{ discussion.content|linebreaks }}
        </div>
    </div>

    <!-- Comments -->
    <div class="space-y-6">
        {% if membership.is_approved %}
        <form method="POST" class="bg-white rounded-lg shadow-md p-6">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary mt-4">Add Comment</button>
        </form>
        {% endif %}

        {% for comment in discussion.comments.all %}
        <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex justify-between items-start">
                <div class="flex items-center space-x-2">
                    <span class="font-semibold">{{ comment.author.username }}</span>
                    <span class="text-gray-500">{{ comment.created_at|timesince }} ago</span>
                </div>
                {% if comment.author == request.user or membership.role in 'founder,moderator' %}
                <button class="text-gray-500 hover:text-red-500" onclick="deleteComment({{ comment.id }})">Delete</button>
                {% endif %}
            </div>
            <div class="mt-2">
                {{ comment.content|linebreaks }}
            </div>
        </div>
        {% empty %}
        <p class="text-center text-gray-500">No comments yet.</p>
        {% endfor %}
    </div>
</div>

<script>
function deleteComment(commentId) {
    if (confirm('Are you sure you want to delete this comment?')) {
        fetch(`/teams/comments/${commentId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                location.reload();
            }
        });
    }
}
</script>
{% endblock %}

# Contents from: .\teams\edit_team.html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<!-- Edit Team Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Edit Team: {{ team.name }}</h1>
        <p class="lead">Update your team's information and settings</p>
    </div>
</div>

<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <!-- Edit Form -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <form method="post" enctype="multipart/form-data" novalidate>
                        {% csrf_token %}
                        
                        <!-- Team Information -->
                        <div class="mb-4">
                            <h5 class="card-title mb-3">
                                <i class="bi bi-info-circle-fill text-primary me-2"></i>
                                Team Information
                            </h5>
                            {{ form.name|as_crispy_field }}
                            {{ form.description|as_crispy_field }}
                        </div>
                        
                        <!-- Team Settings -->
                        <div class="mb-4">
                            <h5 class="card-title mb-3">
                                <i class="bi bi-gear-fill text-primary me-2"></i>
                                Team Settings
                            </h5>
                            {{ form.tags|as_crispy_field }}
                            
                            <!-- Current Image Preview -->
                            {% if team.team_image %}
                            <div class="mb-3">
                                <label class="form-label">Current Team Image</label>
                                <div class="mb-2">
                                    <img src="{{ team.team_image.url }}" 
                                         alt="Current team image" 
                                         class="img-thumbnail"
                                         style="max-width: 200px;">
                                </div>
                            </div>
                            {% endif %}
                            
                            {{ form.team_image|as_crispy_field }}
                        </div>
                        
                        <!-- Action Buttons -->
                        <div class="d-flex justify-content-between">
                            <div>
                                <button type="submit" class="btn btn-primary me-2">
                                    <i class="bi bi-save me-2"></i>Save Changes
                                </button>
                                <a href="{% url 'projects:team_detail' team_slug=team.slug %}" 
                                   class="btn btn-outline-secondary">
                                    <i class="bi bi-x-lg me-2"></i>Cancel
                                </a>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            
            {% if can_delete %}
            <!-- Danger Zone -->
            <div class="card border-danger">
                <div class="card-header bg-danger text-white">
                    <h5 class="card-title mb-0">
                        <i class="bi bi-exclamation-triangle-fill me-2"></i>
                        Danger Zone
                    </h5>
                </div>
                <div class="card-body">
                    <p class="card-text text-danger mb-3">
                        These actions cannot be undone. Please be certain.
                    </p>
                    <form action="{% url 'projects:delete_team' team_slug=team.slug %}" 
                          method="post" 
                          onsubmit="return confirm('Are you sure you want to delete this team? This action cannot be undone.');">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-outline-danger">
                            <i class="bi bi-trash me-2"></i>Delete Team
                        </button>
                    </form>
                </div>
            </div>
            {% endif %}
        </div>
        
        <!-- Help Sidebar -->
        <div class="col-lg-4">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">
                        <i class="bi bi-question-circle-fill text-primary me-2"></i>
                        Tips
                    </h5>
                    <ul class="list-unstyled mb-0">
                        <li class="mb-2">
                            <i class="bi bi-check2 text-success me-2"></i>
                            Use a clear, descriptive team name
                        </li>
                        <li class="mb-2">
                            <i class="bi bi-check2 text-success me-2"></i>
                            Add relevant tags to help others find your team
                        </li>
                        <li class="mb-2">
                            <i class="bi bi-check2 text-success me-2"></i>
                            Upload a team image to make your team stand out
                        </li>
                        <li>
                            <i class="bi bi-check2 text-success me-2"></i>
                            Provide a detailed description of your team's goals
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\teams\leave_team.html
{% extends 'base.html' %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow-sm">
                <div class="card-body text-center">
                    <h1 class="h3 mb-4">Leave Team</h1>
                    <p class="mb-4">Are you sure you want to leave <strong>{{ team.name }}</strong>?</p>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-danger">
                                <i class="bi bi-box-arrow-right me-2"></i>Leave Team
                            </button>
                            <a href="{% url 'projects:team_detail' team_slug=team.slug %}" 
                               class="btn btn-outline-secondary">
                                <i class="bi bi-arrow-left me-2"></i>Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
            
            {% if membership.role != 'founder' %}
            <div class="card mt-4 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">
                        <i class="bi bi-info-circle-fill text-primary me-2"></i>
                        Important Information
                    </h5>
                    <ul class="mb-0">
                        <li>You will lose access to team discussions and resources</li>
                        <li>Your contributions will remain visible to team members</li>
                        <li>You can request to rejoin the team later</li>
                    </ul>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\teams\team_analytics.html
{% extends "base.html" %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-2xl font-bold">{{ team.name }} Analytics</h1>
            <a href="{% url 'team_detail' team.slug %}" class="btn btn-secondary">Back to Team</a>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- Overview Cards -->
            <div class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold text-blue-700">Total Members</h3>
                <p class="text-3xl font-bold">{{ team.member_count }}</p>
                <p class="text-sm text-blue-600">{{ analytics.active_members }} active this month</p>
            </div>

            <div class="bg-green-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold text-green-700">Total Discussions</h3>
                <p class="text-3xl font-bold">{{ analytics.total_discussions }}</p>
                <p class="text-sm text-green-600">{{ analytics.discussions_this_month }} this month</p>
            </div>

            <div class="bg-purple-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold text-purple-700">Total Comments</h3>
                <p class="text-3xl font-bold">{{ analytics.total_comments }}</p>
                <p class="text-sm text-purple-600">{{ analytics.comments_this_month }} this month</p>
            </div>

            <div class="bg-yellow-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold text-yellow-700">Activity Score</h3>
                <p class="text-3xl font-bold">{{ activity_score }}</p>
                <p class="text-sm text-yellow-600">Based on recent activity</p>
            </div>
        </div>

        <!-- Weekly Activity -->
        <div class="mb-8">
            <h2 class="text-xl font-semibold mb-4">Weekly Activity</h2>
            <div class="bg-white rounded-lg p-4 shadow">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <h4 class="font-medium text-gray-700">New Discussions</h4>
                        <p class="text-2xl font-bold">{{ analytics.discussions_this_week }}</p>
                    </div>
                    <div>
                        <h4 class="font-medium text-gray-700">New Comments</h4>
                        <p class="text-2xl font-bold">{{ analytics.comments_this_week }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Member Activity -->
        <div>
            <h2 class="text-xl font-semibold mb-4">Member Activity</h2>
            <div class="bg-white rounded-lg shadow overflow-hidden">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Member</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Discussions</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Comments</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Active</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        {% for member in member_activity %}
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap">{{ member.user.username }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">{{ member.discussions_count }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">{{ member.comments_count }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">{{ member.last_activity|timesince }} ago</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\teams\team_detail.html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<!-- Team Detail Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <div class="d-flex align-items-center">
            {% if team.team_image %}
            <img src="{{ team.team_image.url }}" 
                 alt="{{ team.name }}" 
                 class="rounded-circle me-4"
                 style="width: 100px; height: 100px; object-fit: cover;">
            {% endif %}
            <div>
                <h1 class="display-4">{{ team.name }}</h1>
                <p class="lead mb-0">{{ team.description|truncatewords:30 }}</p>
            </div>
        </div>
    </div>
</div>

<div class="container">
    <div class="row">
        <!-- Main Content -->
        <div class="col-lg-8">
            <!-- Team Actions -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            {% if user_membership %}
                                {% if user_membership.role == 'founder' or user_membership.role == 'moderator' %}
                                <a href="{% url 'projects:edit_team' team_slug=team.slug %}" 
                                   class="btn btn-outline-primary me-2">
                                    <i class="bi bi-pencil me-2"></i>Edit Team
                                </a>
                                {% endif %}
                                <a href="{% url 'projects:leave_team' team_slug=team.slug %}" 
                                   class="btn btn-outline-danger"
                                   onclick="return confirm('Are you sure you want to leave this team?');">
                                    <i class="bi bi-box-arrow-right me-2"></i>Leave Team
                                </a>
                            {% else %}
                                <a href="{% url 'projects:join_team' team_slug=team.slug %}" 
                                   class="btn btn-primary">
                                    <i class="bi bi-person-plus me-2"></i>Join Team
                                </a>
                            {% endif %}
                        </div>
                        
                        {% if user_membership %}
                        <a href="{% url 'projects:team_members' team_slug=team.slug %}" 
                           class="btn btn-outline-secondary">
                            <i class="bi bi-people me-2"></i>View All Members
                        </a>
                        {% endif %}
                    </div>
                </div>
            </div>

            <!-- Team Description -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <h5 class="card-title">About</h5>
                    <p class="card-text">{{ team.description }}</p>
                    
                    {% if tags %}
                    <div class="mt-3">
                        <h6 class="text-muted mb-2">Tags</h6>
                        {% for tag in tags %}
                        <span class="badge bg-light text-dark me-1">{{ tag }}</span>
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
            </div>

            <!-- Team Members Preview -->
            <div class="card shadow-sm">
                <div class="card-header bg-transparent">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Team Members</h5>
                        <span class="badge bg-primary">{{ members.count }} Members</span>
                    </div>
                </div>
                <div class="card-body">
                    {% for member in members|slice:":5" %}
                    <div class="d-flex align-items-center {% if not forloop.last %}mb-3{% endif %}">
                        <img src="{% if member.user.profile.avatar %}{{ member.user.profile.avatar.url }}{% else %}https://via.placeholder.com/40{% endif %}" 
                             class="rounded-circle me-3" 
                             alt="{{ member.user.username }}"
                             style="width: 40px; height: 40px; object-fit: cover;">
                        <div>
                            <h6 class="mb-0">{{ member.user.get_full_name|default:member.user.username }}</h6>
                            <span class="badge {% if member.role == 'founder' %}bg-warning{% elif member.role == 'moderator' %}bg-info{% endif %}">{{ member.role|title }}</span>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- Sidebar -->
        <div class="col-lg-4">
            <!-- Team Members Preview -->
            <div class="card shadow-sm">
                <div class="card-header bg-transparent">
                    <h5 class="mb-0">Team Members</h5>
                </div>
                <div class="card-body">
                    {% for member in members %}
                    <div class="d-flex align-items-center {% if not forloop.last %}mb-3{% endif %}">
                        <img src="{% if member.user.profile.avatar %}{{ member.user.profile.avatar.url }}{% else %}https://via.placeholder.com/40{% endif %}" 
                             class="rounded-circle me-2" 
                             alt="{{ member.user.username }}"
                             style="width: 40px; height: 40px; object-fit: cover;">
                        <div>
                            <h6 class="mb-0">{{ member.user.get_full_name|default:member.user.username }}</h6>
                            <small class="text-muted">{{ member.role|title }}</small>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\teams\team_list.html
{% extends "base.html" %}

{% block content %}
<!-- Teams Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">Teams</h1>
        <p class="lead">Join or create a team to collaborate on projects</p>
    </div>
</div>

<div class="container">
    <!-- Search and Filters -->
    <div class="row mb-4">
        <div class="col-md-8">
            <form method="get" class="d-flex gap-2">
                <div class="flex-grow-1">
                    <div class="input-group">
                        <input type="text" 
                               name="search" 
                               class="form-control" 
                               placeholder="Search teams..."
                               value="{{ search_query }}">
                        <button class="btn btn-outline-secondary" type="submit">
                            <i class="bi bi-search"></i>
                        </button>
                    </div>
                </div>
                
                {% if all_tags %}
                <select name="tag" class="form-select" style="width: auto;" onchange="this.form.submit()">
                    <option value="">All Tags</option>
                    {% for tag in all_tags %}
                    <option value="{{ tag }}" {% if tag == tag_filter %}selected{% endif %}>
                        {{ tag }}
                    </option>
                    {% endfor %}
                </select>
                {% endif %}
            </form>
        </div>
        <div class="col-md-4 text-md-end">
            <a href="{% url 'projects:create_team' %}" class="btn btn-primary">
                <i class="bi bi-plus-lg me-2"></i>Create Team
            </a>
        </div>
    </div>

    <!-- Teams Grid -->
    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        {% for team in teams %}
        <div class="col">
            <div class="card h-100 shadow-sm">
                {% if team.team_image %}
                <img src="{{ team.team_image.url }}" 
                     class="card-img-top" 
                     alt="{{ team.name }}"
                     style="height: 200px; object-fit: cover;">
                {% endif %}
                
                <div class="card-body">
                    <h5 class="card-title">
                        <a href="{% url 'projects:team_detail' team_slug=team.slug %}" 
                           class="text-decoration-none text-dark">
                            {{ team.name }}
                        </a>
                    </h5>
                    <p class="card-text text-muted small">{{ team.description|truncatewords:30 }}</p>
                    
                    {% if team.tags %}
                    <div class="mb-3">
                        {% for tag in team.tags.split|slice:":3" %}
                        <span class="badge bg-light text-dark me-1">{{ tag }}</span>
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
                
                <div class="card-footer bg-transparent">
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            {{ team.memberships.count }} member{{ team.memberships.count|pluralize }}
                        </small>
                        <small class="text-muted">
                            Created {{ team.created_at|timesince }} ago
                        </small>
                    </div>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <div class="text-center py-5">
                {% if search_query or tag_filter %}
                <p class="text-muted mb-0">No teams found matching your search criteria.</p>
                <a href="{% url 'projects:team_list' %}" class="btn btn-outline-primary mt-3">
                    Clear Filters
                </a>
                {% else %}
                <p class="text-muted mb-3">No teams have been created yet.</p>
                <a href="{% url 'projects:create_team' %}" class="btn btn-primary">
                    <i class="bi bi-plus-lg me-2"></i>Create the First Team
                </a>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}

# Contents from: .\teams\team_members.html
{% extends 'base.html' %}

{% block content %}
<!-- Team Members Header -->
<div class="bg-primary text-white py-5 mb-5">
    <div class="container">
        <h1 class="display-4">{{ team.name }} - Members</h1>
        <p class="lead">{{ members.count }} team member{{ members.count|pluralize }}</p>
    </div>
</div>

<div class="container">
    <div class="row">
        <!-- Main Content -->
        <div class="col-lg-8">
            {% if pending_requests %}
            <!-- Pending Requests -->
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-warning bg-opacity-10">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">
                            <i class="bi bi-clock-fill me-2"></i>
                            Pending Requests
                        </h5>
                        <span class="badge bg-warning text-dark">{{ pending_requests.count }}</span>
                    </div>
                </div>
                <div class="card-body">
                    {% for request in pending_requests %}
                    <div class="d-flex justify-content-between align-items-center {% if not forloop.last %}border-bottom pb-3 mb-3{% endif %}">
                        <div class="d-flex align-items-center">
                            <img src="{% if request.user.profile.avatar %}{{ request.user.profile.avatar.url }}{% else %}https://via.placeholder.com/40{% endif %}" 
                                 class="rounded-circle me-3" 
                                 alt="{{ request.user.username }}"
                                 style="width: 40px; height: 40px; object-fit: cover;">
                            <div>
                                <h6 class="mb-0">{{ request.user.get_full_name|default:request.user.username }}</h6>
                                {% if request.user.profile.title %}
                                <small class="text-muted">{{ request.user.profile.title }}</small>
                                {% endif %}
                            </div>
                        </div>
                        <div>
                            <form method="post" action="{% url 'projects:approve_member' team_slug=team.slug user_id=request.user.id %}" class="d-inline">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-success btn-sm me-2">
                                    <i class="bi bi-check-lg me-1"></i>Approve
                                </button>
                            </form>
                            <form method="post" action="{% url 'projects:reject_member' team_slug=team.slug user_id=request.user.id %}" class="d-inline">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-outline-danger btn-sm">
                                    <i class="bi bi-x-lg me-1"></i>Reject
                                </button>
                            </form>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            <!-- Team Members List -->
            <div class="card shadow-sm">
                <div class="card-header bg-transparent">
                    <h5 class="mb-0">Team Members</h5>
                </div>
                <div class="card-body">
                    {% for member in members %}
                    <div class="d-flex justify-content-between align-items-center {% if not forloop.last %}border-bottom pb-3 mb-3{% endif %}">
                        <div class="d-flex align-items-center">
                            <img src="{% if member.user.profile.avatar %}{{ member.user.profile.avatar.url }}{% else %}https://via.placeholder.com/48{% endif %}" 
                                 class="rounded-circle me-3" 
                                 alt="{{ member.user.username }}"
                                 style="width: 48px; height: 48px; object-fit: cover;">
                            <div>
                                <h6 class="mb-0">{{ member.user.get_full_name|default:member.user.username }}</h6>
                                <div>
                                    <span class="badge {% if member.role == 'founder' %}bg-warning{% elif member.role == 'moderator' %}bg-info{% else %}bg-secondary{% endif %} text-dark">
                                        {{ member.role|title }}
                                    </span>
                                    {% if member.user.profile.title %}
                                    <small class="text-muted ms-2">{{ member.user.profile.title }}</small>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        
                        {% if can_manage and member.user != request.user %}
                        <div class="dropdown">
                            <button class="btn btn-outline-secondary btn-sm dropdown-toggle" 
                                    type="button" 
                                    data-bs-toggle="dropdown">
                                Actions
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                {% if user_membership.role == 'founder' and member.role != 'moderator' %}
                                <li>
                                    <form action="{% url 'projects:promote_member' team_slug=team.slug user_id=member.user.id %}" method="post">
                                        {% csrf_token %}
                                        <button type="submit" class="dropdown-item">
                                            <i class="bi bi-arrow-up-circle me-2"></i>Promote to Moderator
                                        </button>
                                    </form>
                                </li>
                                {% endif %}
                                <li>
                                    <form action="{% url 'projects:remove_member' team_slug=team.slug user_id=member.user.id %}" 
                                          method="post"
                                          onsubmit="return confirm('Are you sure you want to remove this member?');">
                                        {% csrf_token %}
                                        <button type="submit" class="dropdown-item text-danger">
                                            <i class="bi bi-person-x me-2"></i>Remove from Team
                                        </button>
                                    </form>
                                </li>
                            </ul>
                        </div>
                        {% endif %}
                    </div>
                    {% empty %}
                    <p class="text-center text-muted my-4">No members found.</p>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <!-- Team Info Sidebar -->
        <div class="col-lg-4">
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <h5 class="card-title">About Team</h5>
                    <p class="card-text">{{ team.description }}</p>
                    {% if tags %}
                    <div class="mb-3">
                        <h6 class="card-subtitle text-muted mb-2">Tags</h6>
                        {% for tag in tags %}
                        <span class="badge bg-light text-dark me-1">{{ tag }}</span>
                        {% endfor %}
                    </div>
                    {% endif %}
                    <div class="mb-0">
                        <h6 class="card-subtitle text-muted mb-2">Quick Stats</h6>
                        <ul class="list-unstyled mb-0">
                            <li class="mb-2">
                                <i class="bi bi-people-fill me-2"></i>
                                {{ members.count }} Members
                            </li>
                            <li>
                                <i class="bi bi-calendar-fill me-2"></i>
                                Created {{ team.created_at|date:"M d, Y" }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- Back to Team -->
            <a href="{% url 'projects:team_detail' team_slug=team.slug %}" 
               class="btn btn-outline-primary w-100">
                <i class="bi bi-arrow-left me-2"></i>Back to Team
            </a>
        </div>
    </div>
</div>
{% endblock %}

# Contents from: .\combine.py
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