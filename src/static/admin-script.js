// Global variables
let currentUser = null;
let applications = [];
let jobs = [];
let dashboardStats = {};

// DOM elements
const loginModal = document.getElementById('login-modal');
const adminDashboard = document.getElementById('admin-dashboard');
const loginForm = document.getElementById('login-form');
const navBtns = document.querySelectorAll('.nav-btn');
const tabContents = document.querySelectorAll('.tab-content');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeAdmin();
});

function initializeAdmin() {
    // Check if already authenticated
    checkAuthentication();
    
    // Setup event listeners
    setupEventListeners();
}

function setupEventListeners() {
    // Login form
    loginForm.addEventListener('submit', handleLogin);
    
    // Navigation tabs
    navBtns.forEach(btn => {
        btn.addEventListener('click', (e) => switchTab(e.target.dataset.tab));
    });
    
    // Search and filters
    const applicationsSearch = document.getElementById('applications-search');
    const statusFilter = document.getElementById('status-filter');
    
    if (applicationsSearch) {
        applicationsSearch.addEventListener('input', filterApplications);
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterApplications);
    }
    
    // Job form
    const jobForm = document.getElementById('job-form');
    if (jobForm) {
        jobForm.addEventListener('submit', handleJobSubmit);
    }
}

async function checkAuthentication() {
    try {
        const response = await fetch('/api/admin/check-auth', {
            credentials: 'include'
        });
        const result = await response.json();
        
        if (result.success && result.authenticated) {
            currentUser = result.user;
            showDashboard();
            loadDashboardData();
        } else {
            showLogin();
        }
    } catch (error) {
        console.error('Error checking authentication:', error);
        showLogin();
    }
}

async function handleLogin(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Show loading state
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connexion...';
    submitBtn.disabled = true;
    
    try {
        const formData = new FormData(loginForm);
        const loginData = {
            username: formData.get('username'),
            password: formData.get('password')
        };
        
        const response = await fetch('/api/admin/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(loginData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentUser = result.user;
            showDashboard();
            loadDashboardData();
            showNotification('Connexion réussie!', 'success');
        } else {
            showNotification(result.message || 'Identifiants invalides', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Erreur de connexion', 'error');
    } finally {
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

async function logout() {
    try {
        await fetch('/api/admin/logout', { method: 'POST' });
        currentUser = null;
        showLogin();
        showNotification('Déconnexion réussie', 'info');
    } catch (error) {
        console.error('Logout error:', error);
    }
}

function showLogin() {
    loginModal.classList.add('active');
    adminDashboard.classList.add('hidden');
    loginForm.reset();
}

function showDashboard() {
    loginModal.classList.remove('active');
    adminDashboard.classList.remove('hidden');
    
    // Update user info
    const usernameSpan = document.getElementById('admin-username');
    if (usernameSpan && currentUser) {
        usernameSpan.textContent = currentUser.username;
    }
}

function switchTab(tabName) {
    // Update navigation
    navBtns.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Update content
    tabContents.forEach(content => content.classList.remove('active'));
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Load tab-specific data
    switch(tabName) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'applications':
            loadApplications();
            break;
        case 'jobs':
            loadJobs();
            break;
    }
}

async function loadDashboardData() {
    try {
        const response = await fetch('/api/admin/stats');
        const result = await response.json();
        
        dashboardStats = result;
        updateDashboardStats();
        
        // Load recent applications
        const appsResponse = await fetch('/api/admin/applications');
        const applications = await appsResponse.json();
        const recentApplications = applications.slice(-5).reverse(); // Last 5 applications
        renderRecentApplications(recentApplications);
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function updateDashboardStats() {
    document.getElementById('total-jobs').textContent = dashboardStats.total_jobs || 0;
    document.getElementById('active-jobs').textContent = dashboardStats.total_jobs || 0; // Same as total for now
    document.getElementById('total-applications').textContent = dashboardStats.total_applications || 0;
    document.getElementById('pending-applications').textContent = dashboardStats.applications_today || 0;
}

function renderRecentApplications(recentApplications) {
    const container = document.getElementById('recent-applications');
    
    if (!recentApplications || recentApplications.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-inbox"></i><p>Aucune candidature récente</p></div>';
        return;
    }
    
    container.innerHTML = recentApplications.map(app => `
        <div class="recent-application">
            <div class="recent-application-info">
                <h4>${app.first_name} ${app.last_name}</h4>
                <p>${app.job_title} • ${formatDate(app.applied_at)}</p>
            </div>
            <div class="recent-application-actions">
                <span class="status-badge status-${app.status.toLowerCase().replace(' ', '-')}">${app.status}</span>
                <button class="btn btn-primary" onclick="viewApplication(${app.id})">
                    <i class="fas fa-eye"></i>
                </button>
            </div>
        </div>
    `).join('');
}

async function loadApplications() {
    try {
        showLoading('applications-list');
        
        const response = await fetch('/api/admin/applications');
        const result = await response.json();
        
        if (Array.isArray(result)) {
            applications = result;
            renderApplications(applications);
        } else {
            showError('applications-list', 'Erreur lors du chargement des candidatures');
        }
    } catch (error) {
        console.error('Error loading applications:', error);
        showError('applications-list', 'Erreur de connexion');
    }
}

function renderApplications(applicationsToRender) {
    const container = document.getElementById('applications-list');
    
    if (!applicationsToRender || applicationsToRender.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-file-alt"></i><p>Aucune candidature trouvée</p></div>';
        return;
    }
    
    container.innerHTML = applicationsToRender.map(app => `
        <div class="application-item">
            <div class="application-info">
                <div class="application-name">${app.first_name} ${app.last_name}</div>
                <div class="application-meta">
                    <span><i class="fas fa-briefcase"></i> ${app.job_title}</span>
                    <span><i class="fas fa-envelope"></i> ${app.email}</span>
                    <span><i class="fas fa-calendar"></i> ${formatDate(app.applied_at)}</span>
                </div>
            </div>
            <div class="application-actions">
                <span class="status-badge status-${app.status.toLowerCase().replace(' ', '-')}">${app.status}</span>
                <button class="btn btn-primary" onclick="viewApplication(${app.id})">
                    <i class="fas fa-eye"></i> Voir
                </button>
            </div>
        </div>
    `).join('');
}

function filterApplications() {
    const searchTerm = document.getElementById('applications-search').value.toLowerCase();
    const statusFilter = document.getElementById('status-filter').value;
    
    let filtered = applications.filter(app => {
        const matchesSearch = !searchTerm || 
            app.first_name.toLowerCase().includes(searchTerm) ||
            app.last_name.toLowerCase().includes(searchTerm) ||
            app.email.toLowerCase().includes(searchTerm) ||
            app.job_title.toLowerCase().includes(searchTerm);
        
        const matchesStatus = !statusFilter || app.status === statusFilter;
        
        return matchesSearch && matchesStatus;
    });
    
    renderApplications(filtered);
}

async function viewApplication(applicationId) {
    try {
        const response = await fetch(`/api/applications/${applicationId}`);
        const result = await response.json();
        
        if (result.success) {
            showApplicationModal(result.application);
        } else {
            showNotification('Erreur lors du chargement de la candidature', 'error');
        }
    } catch (error) {
        console.error('Error loading application:', error);
        showNotification('Erreur de connexion', 'error');
    }
}

function showApplicationModal(application) {
    const modal = document.getElementById('application-modal');
    const detailsContainer = document.getElementById('application-details');
    
    detailsContainer.innerHTML = `
        <div class="application-details">
            <div class="detail-section">
                <h3>Informations personnelles</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <span class="detail-label">Nom complet</span>
                        <span class="detail-value">${application.first_name} ${application.last_name}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Date de naissance</span>
                        <span class="detail-value">${formatDate(application.birth_date)}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Citoyenneté</span>
                        <span class="detail-value">${application.citizenship}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Email</span>
                        <span class="detail-value">${application.email}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Téléphone</span>
                        <span class="detail-value">${application.phone}</span>
                    </div>
                </div>
                <div class="detail-item" style="margin-top: 1rem;">
                    <span class="detail-label">Adresse</span>
                    <span class="detail-value">${application.address}</span>
                </div>
            </div>
            
            <div class="detail-section">
                <h3>Informations sur le poste</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <span class="detail-label">Poste</span>
                        <span class="detail-value">${application.job_title}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Date de candidature</span>
                        <span class="detail-value">${formatDate(application.applied_at)}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Statut</span>
                        <span class="status-badge status-${application.status.toLowerCase().replace(' ', '-')}">${application.status}</span>
                    </div>
                </div>
            </div>
            
            <div class="detail-section">
                <h3>Documents</h3>
                <div class="document-links">
                    <a href="/api/download/${application.id}/document_front" class="document-link" target="_blank">
                        <i class="fas fa-download"></i> Document recto
                    </a>
                    <a href="/api/download/${application.id}/document_back" class="document-link" target="_blank">
                        <i class="fas fa-download"></i> Document verso
                    </a>
                    <a href="/api/download/${application.id}/address_proof" class="document-link" target="_blank">
                        <i class="fas fa-download"></i> Justificatif domicile
                    </a>
                </div>
            </div>
            
            <div class="detail-section">
                <h3>Actions</h3>
                <div class="status-actions">
                    <button class="btn btn-success" onclick="updateApplicationStatus(${application.id}, 'Accepté')">
                        <i class="fas fa-check"></i> Accepter
                    </button>
                    <button class="btn btn-danger" onclick="updateApplicationStatus(${application.id}, 'Refusé')">
                        <i class="fas fa-times"></i> Refuser
                    </button>
                    <button class="btn btn-secondary" onclick="updateApplicationStatus(${application.id}, 'En attente')">
                        <i class="fas fa-clock"></i> En attente
                    </button>
                </div>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
}

async function updateApplicationStatus(applicationId, newStatus) {
    try {
        const response = await fetch(`/api/applications/${applicationId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification(`Statut mis à jour: ${newStatus}`, 'success');
            closeApplicationModal();
            loadApplications(); // Refresh the list
            loadDashboardData(); // Update stats
        } else {
            showNotification(result.message || 'Erreur lors de la mise à jour', 'error');
        }
    } catch (error) {
        console.error('Error updating application status:', error);
        showNotification('Erreur de connexion', 'error');
    }
}

function closeApplicationModal() {
    document.getElementById('application-modal').style.display = 'none';
}

async function loadJobs() {
    try {
        showLoading('jobs-list');
        
        const response = await fetch('/api/jobs');
        const result = await response.json();
        
        if (result.success) {
            jobs = result.jobs;
            renderJobs(jobs);
        } else {
            showError('jobs-list', 'Erreur lors du chargement des offres');
        }
    } catch (error) {
        console.error('Error loading jobs:', error);
        showError('jobs-list', 'Erreur de connexion');
    }
}

function renderJobs(jobsToRender) {
    const container = document.getElementById('jobs-list');
    
    if (!jobsToRender || jobsToRender.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-briefcase"></i><p>Aucune offre d\'emploi trouvée</p></div>';
        return;
    }
    
    container.innerHTML = jobsToRender.map(job => `
        <div class="job-item">
            <div class="job-info">
                <div class="job-title">${job.title}</div>
                <div class="job-meta">
                    <span><i class="fas fa-map-marker-alt"></i> ${job.location}</span>
                    <span><i class="fas fa-building"></i> ${job.department}</span>
                    <span><i class="fas fa-clock"></i> ${job.contract_type}</span>
                    <span><i class="fas fa-users"></i> ${job.applications_count} candidature(s)</span>
                </div>
            </div>
            <div class="job-actions">
                <span class="status-badge status-${job.is_active ? 'active' : 'inactive'}">
                    ${job.is_active ? 'Active' : 'Inactive'}
                </span>
                <button class="btn btn-primary" onclick="editJob(${job.id})">
                    <i class="fas fa-edit"></i> Modifier
                </button>
                <button class="btn btn-danger" onclick="deleteJob(${job.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function openJobModal(jobId = null) {
    const modal = document.getElementById('job-modal');
    const form = document.getElementById('job-form');
    const title = document.getElementById('job-modal-title');
    
    if (jobId) {
        // Edit mode
        const job = jobs.find(j => j.id === jobId);
        if (job) {
            title.textContent = 'Modifier l\'offre d\'emploi';
            populateJobForm(job);
        }
    } else {
        // Create mode
        title.textContent = 'Nouvelle offre d\'emploi';
        form.reset();
        document.getElementById('job-id').value = '';
    }
    
    modal.style.display = 'flex';
}

function populateJobForm(job) {
    document.getElementById('job-id').value = job.id;
    document.getElementById('job-title').value = job.title;
    document.getElementById('job-location').value = job.location;
    document.getElementById('job-department').value = job.department;
    document.getElementById('job-contract').value = job.contract_type;
    document.getElementById('job-experience').value = job.experience_level;
    document.getElementById('job-salary').value = job.salary_range || '';
    document.getElementById('job-description').value = job.description;
    document.getElementById('job-requirements').value = job.requirements;
    document.getElementById('job-benefits').value = job.benefits || '';
}

function editJob(jobId) {
    openJobModal(jobId);
}

async function handleJobSubmit(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Show loading state
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enregistrement...';
    submitBtn.disabled = true;
    
    try {
        const formData = new FormData(e.target);
        const jobData = Object.fromEntries(formData.entries());
        const jobId = jobData.job_id;
        
        // Remove job_id from data
        delete jobData.job_id;
        
        const url = jobId ? `/api/jobs/${jobId}` : '/api/jobs';
        const method = jobId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jobData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification(jobId ? 'Offre mise à jour avec succès!' : 'Offre créée avec succès!', 'success');
            closeJobModal();
            loadJobs(); // Refresh the list
            loadDashboardData(); // Update stats
        } else {
            showNotification(result.message || 'Erreur lors de l\'enregistrement', 'error');
        }
    } catch (error) {
        console.error('Error saving job:', error);
        showNotification('Erreur de connexion', 'error');
    } finally {
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

async function deleteJob(jobId) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette offre d\'emploi ?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/jobs/${jobId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('Offre supprimée avec succès!', 'success');
            loadJobs(); // Refresh the list
            loadDashboardData(); // Update stats
        } else {
            showNotification(result.message || 'Erreur lors de la suppression', 'error');
        }
    } catch (error) {
        console.error('Error deleting job:', error);
        showNotification('Erreur de connexion', 'error');
    }
}

function closeJobModal() {
    document.getElementById('job-modal').style.display = 'none';
}

// Utility functions
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
}

function showError(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `<div class="empty-state"><i class="fas fa-exclamation-triangle"></i><p>${message}</p></div>`;
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('fr-FR', options);
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Global functions
window.logout = logout;
window.viewApplication = viewApplication;
window.updateApplicationStatus = updateApplicationStatus;
window.closeApplicationModal = closeApplicationModal;
window.openJobModal = openJobModal;
window.editJob = editJob;
window.deleteJob = deleteJob;
window.closeJobModal = closeJobModal;

