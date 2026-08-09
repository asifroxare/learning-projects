document.addEventListener('DOMContentLoaded', function() {
    
    // Select all section elements inside <main>
    const allSections = document.querySelectorAll('main > section');
    const navLinks = document.querySelectorAll('header nav a');

    function showOnlySection(targetId) {
        if (targetId === 'home') {
            // SHOW ALL SECTIONS FOR HOME
            allSections.forEach(section => {
                section.style.display = 'block';
            });
        } else {
            // HIDE ALL SECTIONS FIRST
            allSections.forEach(section => {
                section.style.display = 'none';
            });

            // SHOW ONLY THE SPECIFIC CLICKED SECTION
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.style.display = 'block';
            }
        }
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Attach click listeners to Header Nav Links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.replace('#', '');
                showOnlySection(targetId);
            }
        });
    });

    // Attach click listeners to internal Buttons (like Enroll Now / Contact Us)
    const actionBtns = document.querySelectorAll('a.btn[href^="#"]');
    actionBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.replace('#', '');
                showOnlySection(targetId);
            }
        });
    });

    // --- Tab Switching Logic (UG / PG inside Syllabus) ---
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');

            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            this.classList.add('active');
            const targetEl = document.getElementById(targetTab);
            if (targetEl) targetEl.classList.add('active');
        });
    });

    // --- Accordion Toggle Logic ---
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const item = this.parentElement;
            const parentAccordion = item.parentElement;
            
            // Close other open accordions in the same list
            parentAccordion.querySelectorAll('.accordion-item').forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('open');
                }
            });

            // Toggle current accordion item
            item.classList.toggle('open');
        });
    });
});