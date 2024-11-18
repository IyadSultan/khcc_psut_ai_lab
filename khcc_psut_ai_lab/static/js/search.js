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