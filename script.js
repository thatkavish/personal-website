// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Typewriter effect for tagline
const tagline = document.querySelector('.tagline');
const text = tagline.textContent;
tagline.textContent = '';

let charIndex = 0;
function typeWriter() {
    if (charIndex < text.length) {
        tagline.textContent += text.charAt(charIndex);
        charIndex++;
        setTimeout(typeWriter, 50);
    }
}

// Start typewriter effect after name animation
setTimeout(typeWriter, 2000);

// Navbar scroll effect with academic style
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        navbar.style.borderBottom = '1px solid rgba(212, 175, 55, 0.1)';
    } else {
        navbar.style.borderBottom = '1px solid rgba(212, 175, 55, 0.3)';
    }
    
    lastScroll = currentScroll;
});

// Book hover effect
document.querySelectorAll('.book-card').forEach(book => {
    book.addEventListener('mouseenter', () => {
        book.style.transform = 'translateY(-10px) rotateY(10deg)';
    });
    
    book.addEventListener('mouseleave', () => {
        book.style.transform = 'translateY(0) rotateY(0)';
    });
});

// Blog card hover effect
document.querySelectorAll('.blog-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-5px)';
        card.style.borderColor = 'var(--accent-color)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
        card.style.borderColor = 'rgba(212, 175, 55, 0.1)';
    });
});

// Research card interaction
document.querySelectorAll('.research-card').forEach(card => {
    card.addEventListener('click', () => {
        card.classList.add('pulse');
        setTimeout(() => {
            card.classList.remove('pulse');
        }, 1000);
    });
});

// Add CSS for research card pulse animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 1s ease-in-out;
    }
`;
document.head.appendChild(style);

// Mobile menu functionality
const createMobileMenu = () => {
    const nav = document.querySelector('.nav-content');
    const menuButton = document.createElement('button');
    menuButton.className = 'mobile-menu-button';
    menuButton.innerHTML = '<i class="fas fa-bars"></i>';
    menuButton.style.display = 'none';

    const navLinks = document.querySelector('.nav-links');
    nav.insertBefore(menuButton, navLinks);

    menuButton.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        menuButton.innerHTML = navLinks.classList.contains('active') 
            ? '<i class="fas fa-times"></i>' 
            : '<i class="fas fa-bars"></i>';
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!nav.contains(e.target) && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            menuButton.innerHTML = '<i class="fas fa-bars"></i>';
        }
    });
};

createMobileMenu();
