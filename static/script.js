/**
 * EchoBridge - Premium Animations Script
 */

// ========================================
// Translations Dictionary
// ========================================
const translations = {
    en: {
        // Navigation
        nav_home: "Home",
        nav_stats: "Stats",
        nav_how_it_works: "How It Works",
        nav_features: "Features",
        nav_privacy: "Privacy",
        nav_login: "Login",
        nav_logout: "Logout",
        
        // Hero Section
        hero_title: "Connect Beyond Words",
        hero_subtitle: "AI-powered emotion-based human connection platform. Experience genuine interactions through emotion-aware technology.",
        hero_detect: "Detect Emotion",
        hero_select: "Select Manually",
        hero_badge_privacy: "Privacy First",
        hero_badge_realtime: "Real-time Detection",
        hero_badge_ai: "AI Powered",
        
        // Stats Section
        stats_emotions: "Emotions Analyzed",
        stats_accuracy: "Detection Accuracy (%)",
        stats_connections: "Connections Made",
        stats_privacy: "Privacy Score (%)",
        
        // How It Works
        how_title: "Connect Through Emotions",
        how_desc: "Three simple steps to find your emotional match",
        step1_title: "Detect Emotion",
        step1_desc: "Our AI analyzes your facial expressions in real-time or select your current mood manually.",
        step2_title: "Smart Matching",
        step2_desc: "Connect with people who share similar emotional states for genuine understanding.",
        step3_title: "Secure Chat",
        step3_desc: "Enjoy anonymous, encrypted conversations in a safe, private environment.",
        
        // Features
        features_title: "Why Choose EchoBridge",
        features_desc: "Built with privacy and user experience in mind",
        feature_emotion: "Emotion Detection",
        feature_emotion_desc: "Advanced AI analyzes 7 basic emotions with high accuracy in real-time.",
        feature_privacy: "Privacy First",
        feature_privacy_desc: "No images stored. Your facial data is processed locally and immediately discarded.",
        feature_multilang: "Multi-Language",
        feature_multilang_desc: "Connect with people globally. Support for multiple languages.",
        feature_instant: "Instant Matching",
        feature_instant_desc: "Find your emotional match within seconds. No waiting, just connection.",
        feature_manual: "Manual Selection",
        feature_manual_desc: "Choose your emotion manually if you prefer not to use camera access.",
        feature_genuine: "Genuine Connections",
        feature_genuine_desc: "Connect based on emotional compatibility for meaningful conversations.",
        
        // CTA Section
        cta_title: "Ready to Connect?",
        cta_desc: "Join thousands of people discovering genuine emotional connections.",
        cta_get_started: "Get Started",
        cta_learn_more: "Learn More",
        
        // Footer
        footer_product: "Product",
        footer_legal: "Legal",
        footer_connect: "Connect",
        footer_home: "Home",
        footer_how: "How It Works",
        footer_features: "Features",
        footer_privacy: "Privacy Policy",
        footer_terms: "Terms of Service",
        footer_cookie: "Cookie Policy",
        footer_contact: "Contact Us",
        footer_copyright: "2026 EchoBridge AI. All rights reserved.",
        footer_made: "Made for emotional connection"
    },
    hi: {
        // Navigation
        nav_home: "होम",
        nav_stats: "आंकड़े",
        nav_how_it_works: "कैसे काम करता है",
        nav_features: "विशेषताएं",
        nav_privacy: "गोपनीयता",
        nav_login: "लॉगिन",
        nav_logout: "लॉगआउट",
        
        // Hero Section
        hero_title: "शब्दों से आगे जुड़ें",
        hero_subtitle: "AI-संचालित भावना-आधारित मानव कनेक्शन प्लेटफॉर्म। भावना-जागरूक तकनीक के माध्यम से प्रामाणिक बातचीत का अनुभव करें।",
        hero_detect: "भावना पहचानें",
        hero_select: "मैन्युअल रूप से चुनें",
        hero_badge_privacy: "गोपनीयता पहले",
        hero_badge_realtime: "रीयल-टाइम पहचान",
        hero_badge_ai: "AI संचालित",
        
        // Stats Section
        stats_emotions: "विश्लेषण की गई भावनाएं",
        stats_accuracy: "पहचान सटीकता (%)",
        stats_connections: "बने कनेक्शन",
        stats_privacy: "गोपनीयता स्कोर (%)",
        
        // How It Works
        how_title: "भावनाओं से जुड़ें",
        how_desc: "अपना भावनात्मक मैच खोजने के तीन सरल चरण",
        step1_title: "भावना पहचानें",
        step1_desc: "हमारा AI आपके चेहरे के भावों का वास्तविक समय में विश्लेषण करता है।",
        step2_title: "स्मार्ट मैचिंग",
        step2_desc: "उन लोगों से जुड़ें जो समान भावनात्मक स्थिति साझा करते हैं।",
        step3_title: "सुरक्षित चैट",
        step3_desc: "एक सुरक्षित, निजी वातावरण में बातचीत का आनंद लें।",
        
        // Features
        features_title: "EchoBridge क्यों चुनें",
        features_desc: "गोपनीयता और उपयोगकर्ता अनुभव को ध्यान में रखकर बनाया गया",
        feature_emotion: "भावना पहचान",
        feature_emotion_desc: "उन्नत AI 7 मूल भावनाओं का वास्तविक समय में विश्लेषण करता है।",
        feature_privacy: "गोपनीयता पहले",
        feature_privacy_desc: "कोई छवि संग्रहीत नहीं। आपका डेटा स्थानीय रूप से संसाधित होता है।",
        feature_multilang: "बहुभाषी",
        feature_multilang_desc: "दुनिया भर के लोगों से जुड़ें।",
        feature_instant: "त्वरित मैचिंग",
        feature_instant_desc: "सेकंड में अपना भावनात्मक मैच खोजें।",
        feature_manual: "मैन्युअल चयन",
        feature_manual_desc: "अपनी भावना मैन्युअल रूप से चुनें।",
        feature_genuine: "प्रामाणिक कनेक्शन",
        feature_genuine_desc: "भावनात्मक अनुकूलता के आधार पर जुड़ें।",
        
        // CTA Section
        cta_title: "जुड़ने के लिए तैयार?",
        cta_desc: "प्रामाणिक भावनात्मक कनेक्शन खोजने वाले हजारों लोगों में शामिल हों।",
        cta_get_started: "शुरू करें",
        cta_learn_more: "और जानें",
        
        // Footer
        footer_product: "उत्पाद",
        footer_legal: "कानूनी",
        footer_connect: "जुड़ें",
        footer_home: "होम",
        footer_how: "कैसे काम करता है",
        footer_features: "विशेषताएं",
        footer_privacy: "गोपनीयता नीति",
        footer_terms: "सेवा की शर्तें",
        footer_cookie: "कुकी नीति",
        footer_contact: "संपर्क करें",
        footer_copyright: "2026 EchoBridge AI. सर्वाधिकार सुरक्षित।",
        footer_made: "भावनात्मक कनेक्शन के लिए बनाया गया"
    },
    te: {
        // Navigation
        nav_home: "హోం",
        nav_stats: "గణాంకాలు",
        nav_how_it_works: "ఎలా పనిచేస్తుంది",
        nav_features: "లక్షణాలు",
        nav_privacy: "గోప్యత",
        nav_login: "లాగిన్",
        nav_logout: "లాగౌట్",
        
        // Hero Section
        hero_title: "కాదలు కంటె ఎక్కువగా కనెక్ట్",
        hero_subtitle: "AI-శక్తితో భావన-ఆధారిత మానవ కనెక్షన్ প্ল্যাট్‌ఫామ్.",
        hero_detect: "భావనను గుర్తించు",
        hero_select: "manuel ga select cheyyi",
        hero_badge_privacy: "গোপনীয়তा",
        hero_badge_realtime: "Real-time Detection",
        hero_badge_ai: "AI Powered",
        
        // Stats Section
        stats_emotions: "Emotions Analyzed",
        stats_accuracy: "Detection Accuracy (%)",
        stats_connections: "Connections Made",
        stats_privacy: "Privacy Score (%)",
        
        // How It Works
        how_title: "Connect Through Emotions",
        how_desc: "Three simple steps to find your emotional match",
        step1_title: "Detect Emotion",
        step1_desc: "Our AI analyzes your facial expressions in real-time.",
        step2_title: "Smart Matching",
        step2_desc: "Connect with people who share similar emotional states.",
        step3_title: "Secure Chat",
        step3_desc: "Enjoy anonymous conversations in a safe environment.",
        
        // Features
        features_title: "EchoBridge choose cheyyali",
        features_desc: "Built with privacy and user experience in mind",
        feature_emotion: "Emotion Detection",
        feature_emotion_desc: "Advanced AI analyzes 7 basic emotions.",
        feature_privacy: "Privacy First",
        feature_privacy_desc: "No images stored. Data processed locally.",
        feature_multilang: "Multi-Language",
        feature_multilang_desc: "Connect with people globally.",
        feature_instant: "Instant Matching",
        feature_instant_desc: "Find your emotional match within seconds.",
        feature_manual: "Manual Selection",
        feature_manual_desc: "Choose your emotion manually.",
        feature_genuine: "Genuine Connections",
        feature_genuine_desc: "Connect based on emotional compatibility.",
        
        // CTA Section
        cta_title: "Ready to Connect?",
        cta_desc: "Join thousands of people discovering genuine connections.",
        cta_get_started: "Get Started",
        cta_learn_more: "Learn More",
        
        // Footer
        footer_product: "Product",
        footer_legal: "Legal",
        footer_connect: "Connect",
        footer_home: "Home",
        footer_how: "How It Works",
        footer_features: "Features",
        footer_privacy: "Privacy Policy",
        footer_terms: "Terms of Service",
        footer_cookie: "Cookie Policy",
        footer_contact: "Contact Us",
        footer_copyright: "2026 EchoBridge AI. All rights reserved.",
        footer_made: "Made for emotional connection"
    }
};

// ========================================
// Apply Language Function (Global)
// ========================================
function applyLanguage(lang) {
    console.log('Applying language:', lang);
    if (!translations[lang]) {
        console.error('Language not supported:', lang);
        return;
    }
    
    const trans = translations[lang];
    const translatableElements = document.querySelectorAll('[data-translate]');
    console.log('Found elements to translate:', translatableElements.length);
    
    translatableElements.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (trans[key]) {
            element.textContent = trans[key];
        }
    });
}

// ========================================
// Get Current Language
// ========================================
function getCurrentLanguage() {
    return localStorage.getItem('echobridge_lang') || 'en';
}

// ========================================
// Initialize Translations on Load
// ========================================
function initTranslations() {
    const savedLang = getCurrentLanguage();
    console.log('Initializing translations with language:', savedLang);
    applyLanguage(savedLang);
    
    // Update language dropdown display
    const currentLangEl = document.getElementById('currentLang');
    if (currentLangEl) {
        const option = document.querySelector(`.lang-option[data-lang="${savedLang}"]`);
        if (option) {
            currentLangEl.textContent = option.querySelector('.lang-name').textContent;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize translations
    initTranslations();
    
    // ========================================
    // Scroll Reveal Animation
    // ========================================
    
    const revealElements = document.querySelectorAll('.reveal');
    
    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        const revealPoint = 80;
        
        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            
            if (elementTop < windowHeight - revealPoint) {
                element.classList.add('active');
                
                // Animate counters if present
                const counter = element.querySelector('.counter');
                if (counter && !counter.classList.contains('animated')) {
                    counter.classList.add('animated');
                    const target = parseInt(counter.getAttribute('data-target'));
                    animateCounter(counter, target);
                }
            }
        });
    };
    
    // Initial check for elements already in viewport
    revealOnScroll();
    
    // Scroll event listener with requestAnimationFrame
    let scrollTimeout;
    window.addEventListener('scroll', () => {
        if (scrollTimeout) {
            window.cancelAnimationFrame(scrollTimeout);
        }
        scrollTimeout = window.requestAnimationFrame(revealOnScroll);
    });
    
    // Counter animation function
    function animateCounter(element, target) {
        let current = 0;
        const duration = 2000;
        const stepTime = 20;
        const increment = target / (duration / stepTime);
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target.toLocaleString();
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current).toLocaleString();
            }
        }, stepTime);
    }
    
    // ========================================
    // Navigation Toggle (Mobile)
    // ========================================
    
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            
            const spans = navToggle.querySelectorAll('span');
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
        
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
        
        document.addEventListener('click', (e) => {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }
    
    // ========================================
    // Language Dropdown
    // ========================================
    
    const langBtn = document.getElementById('langBtn');
    const langDropdown = document.getElementById('langDropdown');
    
    if (langBtn && langDropdown) {
        const currentLang = document.getElementById('currentLang');
        const langOptions = document.querySelectorAll('.lang-option');
        
        langBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            langDropdown.classList.toggle('show');
            langBtn.classList.toggle('active');
        });
        
        langOptions.forEach(option => {
            option.addEventListener('click', () => {
                const lang = option.dataset.lang;
                const langName = option.querySelector('.lang-name').textContent;
                if (currentLang) {
                    currentLang.textContent = langName;
                }
                langDropdown.classList.remove('show');
                langBtn.classList.remove('active');
                localStorage.setItem('echobridge_lang', lang);
                
                // Apply translations when language changes
                applyLanguage(lang);
            });
        });
        
        document.addEventListener('click', (e) => {
            if (!langBtn.contains(e.target) && !langDropdown.contains(e.target)) {
                langDropdown.classList.remove('show');
                langBtn.classList.remove('active');
            }
        });
        
        // Load saved language
        const savedLang = localStorage.getItem('echobridge_lang');
        if (savedLang && currentLang) {
            const option = document.querySelector(`.lang-option[data-lang="${savedLang}"]`);
            if (option) {
                currentLang.textContent = option.querySelector('.lang-name').textContent;
            }
        }
    }
    
    // ========================================
    // Smooth Scroll for Navigation Links
    // ========================================
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const navbarHeight = document.querySelector('.navbar').offsetHeight;
                    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
                    
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
    
    const navbar = document.querySelector('.navbar');
    
    const updateNavbar = () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(15, 23, 42, 0.98)';
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
        } else {
            navbar.style.background = 'rgba(15, 23, 42, 0.9)';
            navbar.style.boxShadow = 'none';
        }
    };
    
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

