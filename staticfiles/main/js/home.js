function navigateToSection(section) {
    // Add navigation logic here
    console.log('Navigating to:', section);
    
    if (section === 'sargyt') {
        // This will be handled by Django template URL tag
        window.location.href = sargytUrl;
    } else {
        // For other sections, you can add their URLs here
        alert('Этот раздел находится в разработке...');
    }
}

// Add some interactive effects
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.section').forEach(section => {
        section.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        section.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});
