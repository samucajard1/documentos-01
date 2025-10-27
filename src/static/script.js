// Global variables
let currentJobs = [];
let filteredJobs = [];
let currentCarouselIndex = 0;

// Função para calcular quantas vagas mostrar por vez
function getJobsPerView() {
    const width = window.innerWidth;
    if (width <= 480) return 1;      // Mobile: 1 vaga
    if (width <= 768) return 2;      // Tablet: 2 vagas  
    return 3;                        // Desktop: 3 vagas
}

// Função para calcular largura do card + gap
function getCardWidth() {
    const width = window.innerWidth;
    if (width <= 480) return 280; // Mobile: 260px card + 20px gap
    if (width <= 768) return 300; // Tablet: 280px card + 20px gap  
    return 344;                   // Desktop: 320px card + 24px gap
}

// DOM elements
const jobCarousel = document.getElementById('job-carousel');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const filterBtns = document.querySelectorAll('.filter-btn');
const applicationModal = document.getElementById('application-modal');
const applicationForm = document.getElementById('application-form');
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');

// Load jobs from API
async function loadJobsFromAPI() {
    try {
        const response = await fetch('/api/jobs');
        if (response.ok) {
            const jobs = await response.json();
            currentJobs = jobs;
            filteredJobs = [...jobs];
            renderJobs();
            populateJobSelection();
        } else {
            console.error('Failed to load jobs from API');
            // Fallback to sample data if API fails
            loadSampleJobs();
        }
    } catch (error) {
        console.error('Error loading jobs:', error);
        // Fallback to sample data if API fails
        loadSampleJobs();
    }
}

// Fallback sample jobs
function loadSampleJobs() {
    currentJobs = [
        {
            id: 1,
            title: "Ingénieur Aérodynamique Senior",
            location: "Toulouse",
            department: "Ingénierie",
            type: "CDI",
            description: "Rejoignez notre équipe d'ingénierie aérodynamique pour développer les technologies de demain dans l'aviation commerciale.",
            requirements: "Master en ingénierie aéronautique, 5+ ans d'expérience",
            salary: "55,000 - 75,000 €"
        },
        {
            id: 2,
            title: "Technicien de Production A350",
            location: "Toulouse",
            department: "Production",
            type: "CDI",
            description: "Participez à l'assemblage final de l'A350, l'avion le plus moderne de notre flotte.",
            requirements: "Formation technique, expérience en aéronautique souhaitée",
            salary: "35,000 - 45,000 €"
        }
    ];
    filteredJobs = [...currentJobs];
    renderJobs();
    populateJobSelection();
}

// Render jobs in carousel
function renderJobs() {
    if (!jobCarousel) return;
    
    jobCarousel.innerHTML = '';
    
    filteredJobs.forEach(job => {
        const jobCard = createJobCard(job);
        jobCarousel.appendChild(jobCard);
    });
    
    updateCarouselPosition();
}

// Create job card element
function createJobCard(job) {
    const card = document.createElement('div');
    card.className = 'job-card';
    
    // Mapear imagens para cada vaga
    const jobImages = {
        1: 'job-aerodynamics.png',
        2: 'job-production.jpg', 
        3: 'job-cybersecurity.jpg',
        4: 'job-satellite.jpg',
        5: 'job-helicopter.jpg',
        6: 'job-finance.png',
        7: 'job-innovation.jpg',
        8: 'job-maintenance.jpg'
    };
    
    const imageSrc = jobImages[job.id] || 'G6xAQPV6FlXk.png';
    
    card.innerHTML = `
        <div class="job-image">
            <img src="${imageSrc}" alt="${job.title}" loading="lazy">
        </div>
        <div class="job-content">
            <h3 class="job-title">${job.title}</h3>
            <div class="job-meta">
                <span>${job.location}</span>
                <span>${job.department}</span>
                <span>${job.type}</span>
            </div>
            <p class="job-description">${job.description}</p>
            <p class="job-requirements"><strong>Exigences:</strong> ${job.requirements}</p>
            <p class="job-salary"><strong>Salaire:</strong> ${job.salary}</p>
            <button class="job-apply-btn" onclick="openApplicationModal(${job.id})">
                Postuler
            </button>
        </div>
    `;
    
    return card;
}

// Filter jobs by category
function filterJobs(category) {
    if (category === 'all') {
        filteredJobs = [...currentJobs];
    } else {
        filteredJobs = currentJobs.filter(job => {
            const jobCategory = getDepartmentCategory(job.department);
            return jobCategory === category;
        });
    }
    
    currentCarouselIndex = 0;
    renderJobs();
}

// Get department category
function getDepartmentCategory(department) {
    const departmentMap = {
        'Ingénierie': 'ingenierie',
        'R&D': 'ingenierie',
        'Defence & Space': 'ingenierie',
        'Production': 'production',
        'Maintenance': 'production',
        'Qualité': 'production',
        'IT': 'support',
        'Finance': 'support'
    };
    
    return departmentMap[department] || 'support';
}

// Carousel navigation
function moveCarousel(direction) {
    const jobsPerView = getJobsPerView();
    const maxIndex = Math.max(0, filteredJobs.length - jobsPerView);
    
    if (direction === 'next') {
        currentCarouselIndex = Math.min(currentCarouselIndex + 1, maxIndex);
    } else {
        currentCarouselIndex = Math.max(currentCarouselIndex - 1, 0);
    }
    
    updateCarouselPosition();
}

// Update carousel position
function updateCarouselPosition() {
    if (!jobCarousel) return;
    
    const cardWidth = getCardWidth();
    const translateX = -currentCarouselIndex * cardWidth;
    jobCarousel.style.transform = `translateX(${translateX}px)`;
    
    // Update button states
    const jobsPerView = getJobsPerView();
    if (prevBtn) prevBtn.disabled = currentCarouselIndex === 0;
    if (nextBtn) nextBtn.disabled = currentCarouselIndex >= Math.max(0, filteredJobs.length - jobsPerView);
}

// Modal functions
function openApplicationModal(jobId = null) {
    if (!applicationModal) return;
    
    if (jobId) {
        const job = currentJobs.find(j => j.id === jobId);
        if (job) {
            const jobIdInput = document.getElementById('job_id');
            if (jobIdInput) jobIdInput.value = jobId;
        }
    }
    
    applicationModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    if (applicationModal) {
        applicationModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Populate job selection dropdown
function populateJobSelection() {
    const jobSelect = document.getElementById('job_selection');
    if (jobSelect && currentJobs.length > 0) {
        jobSelect.innerHTML = '<option value="">Sélectionnez un poste</option>';
        
        currentJobs.forEach(job => {
            const option = document.createElement('option');
            option.value = job.id;
            option.textContent = `${job.title} - ${job.location}`;
            jobSelect.appendChild(option);
        });
    }
}

// Form submission function
async function submitApplication(formData, isModal = false) {
    try {
        console.log('Sending FormData with files...');
        
        // Send FormData directly (includes files)
        const response = await fetch('/api/applications', {
            method: 'POST',
            body: formData  // Send FormData directly, don't set Content-Type header
        });
        
        const result = await response.json();
        console.log('Response:', result);
        
        if (response.ok && result.success) {
            if (isModal) closeModal();
            showSuccessMessage();
            return true;
        } else {
            throw new Error(result.message || result.error || 'Erreur lors de l\'envoi');
        }
    } catch (error) {
        console.error('Error:', error);
        showErrorMessage(error.message);
        return false;
    }
}

// Show success message
function showSuccessMessage() {
    const overlay = document.createElement('div');
    overlay.className = 'success-overlay';
    overlay.innerHTML = `
        <div class="success-message">
            <div class="success-icon">
                <i class="fas fa-check"></i>
            </div>
            <h3 class="success-title">Candidature envoyée!</h3>
            <p class="success-text">Votre candidature a été envoyée avec succès. Notre équipe RH vous contactera bientôt.</p>
            <button class="success-btn" onclick="hideSuccessMessage()">Parfait!</button>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    setTimeout(() => {
        overlay.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        hideSuccessMessage();
    }, 5000);
}

// Show error message
function showErrorMessage(message) {
    const overlay = document.createElement('div');
    overlay.className = 'success-overlay';
    overlay.innerHTML = `
        <div class="success-message">
            <div class="success-icon" style="background: #ef4444;">
                <i class="fas fa-times"></i>
            </div>
            <h3 class="success-title">Erreur</h3>
            <p class="success-text">${message}</p>
            <button class="success-btn" style="background: #ef4444;" onclick="hideSuccessMessage()">Réessayer</button>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    setTimeout(() => {
        overlay.classList.add('show');
    }, 100);
}

// Hide success/error message
function hideSuccessMessage() {
    const overlay = document.querySelector('.success-overlay');
    if (overlay) {
        overlay.classList.remove('show');
        setTimeout(() => {
            overlay.remove();
        }, 300);
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Load jobs
    loadJobsFromAPI();
    
    // Filter buttons
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterJobs(btn.dataset.filter);
        });
    });
    
    // Carousel buttons
    if (prevBtn) prevBtn.addEventListener('click', () => moveCarousel('prev'));
    if (nextBtn) nextBtn.addEventListener('click', () => moveCarousel('next'));
    
    // Mobile navigation
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
    
    // Modal close on background click
    if (applicationModal) {
        applicationModal.addEventListener('click', (e) => {
            if (e.target === applicationModal) {
                closeModal();
            }
        });
    }
    
    // Handle modal form submission
    const modalForm = document.getElementById('application-form');
    if (modalForm) {
        modalForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = modalForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.classList.add('btn-loading');
            submitBtn.disabled = true;
            
            const formData = new FormData(modalForm);
            const success = await submitApplication(formData, true);
            
            if (success) {
                modalForm.reset();
            }
            
            submitBtn.classList.remove('btn-loading');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        });
    }
    
    // Handle main application form submission
    const mainApplicationForm = document.getElementById('mainApplicationForm');
    if (mainApplicationForm) {
        mainApplicationForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = mainApplicationForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.classList.add('btn-loading');
            submitBtn.disabled = true;
            
            const formData = new FormData(mainApplicationForm);
            const success = await submitApplication(formData, false);
            
            if (success) {
                mainApplicationForm.reset();
                populateJobSelection();
            }
            
            submitBtn.classList.remove('btn-loading');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        });
    }
});

// Header scroll effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (header) {
        if (window.scrollY > 100) {
            header.style.background = 'rgba(255, 255, 255, 0.98)';
            header.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
        } else {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
            header.style.boxShadow = 'none';
        }
    }
});

// Global functions
window.openApplicationModal = openApplicationModal;
window.closeModal = closeModal;
window.hideSuccessMessage = hideSuccessMessage;

