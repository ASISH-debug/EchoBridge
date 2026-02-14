/**
 * EchoBridge Privacy - Monochrome Script
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // Scroll Reveal Animation
    // ========================================
    
    var revealElements = document.querySelectorAll('.reveal');
    
    function revealOnScroll() {
        var windowHeight = window.innerHeight;
        var revealPoint = 80;
        
        revealElements.forEach(function(element) {
            var elementTop = element.getBoundingClientRect().top;
            
            if (elementTop < windowHeight - revealPoint) {
                element.classList.add('active');
            }
        });
    }
    
    // Initial check
    revealOnScroll();
    
    // Scroll event listener
    var scrollTimeout;
    window.addEventListener('scroll', function() {
        if (scrollTimeout) {
            window.cancelAnimationFrame(scrollTimeout);
        }
        scrollTimeout = window.requestAnimationFrame(revealOnScroll);
    });
    
    // ========================================
    // Navigation Toggle (Mobile)
    // ========================================
    
    var navToggle = document.getElementById('navToggle');
    var navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            
            var spans = navToggle.querySelectorAll('span');
            if (navMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
        
        var navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                var spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
        
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                var spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }
    
    // ========================================
    // Language Dropdown
    // ========================================
    
    var langBtn = document.getElementById('langBtn');
    var langDropdown = document.getElementById('langDropdown');
    
    if (langBtn && langDropdown) {
        var currentLang = document.getElementById('currentLang');
        var langOptions = document.querySelectorAll('.lang-option');
        
        langBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            langDropdown.classList.toggle('show');
            langBtn.classList.toggle('active');
        });
        
        langOptions.forEach(function(option) {
            option.addEventListener('click', function() {
                var lang = this.dataset.lang;
                var langName = this.querySelector('.lang-name').textContent;
                if (currentLang) {
                    currentLang.textContent = langName;
                }
                langDropdown.classList.remove('show');
                langBtn.classList.remove('active');
                localStorage.setItem('echobridge_lang', lang);
            });
        });
        
        document.addEventListener('click', function(e) {
            if (!langBtn.contains(e.target) && !langDropdown.contains(e.target)) {
                langDropdown.classList.remove('show');
                langBtn.classList.remove('active');
            }
        });
        
        // Load saved language
        var savedLang = localStorage.getItem('echobridge_lang');
        if (savedLang && currentLang) {
            var option = document.querySelector('.lang-option[data-lang="' + savedLang + '"]');
            if (option) {
                currentLang.textContent = option.querySelector('.lang-name').textContent;
            }
        }
    }
    
    // ========================================
    // Smooth Scroll for Navigation Links
    // ========================================
    
    var anchors = document.querySelectorAll('a[href^="#"]');
    anchors.forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            var href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                var target = document.querySelector(href);
                if (target) {
                    var navbar = document.querySelector('.navbar');
                    var navbarHeight = navbar.offsetHeight;
                    var targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // ========================================
    // Navbar Background on Scroll
    // ========================================
    
    var navbar = document.querySelector('.navbar');
    
    function updateNavbar() {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(0, 0, 0, 0.95)';
        } else {
            navbar.style.background = 'rgba(0, 0, 0, 0.8)';
        }
    }
    
    window.addEventListener('scroll', updateNavbar);
    updateNavbar();
    
    // ========================================
    // Force Scroll to Top on Page Load
    // ========================================
    
    window.scrollTo(0, 0);
    
    if (window.location.hash) {
        history.pushState("", document.title, window.location.pathname + window.location.search);
    }
    
});

