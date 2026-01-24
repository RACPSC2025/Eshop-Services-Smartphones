/**
 * Router System - SPA Navigation
 * Handles view switching and navigation history
 */

class Router {
  constructor() {
    this.routes = new Map();
    this.currentView = 'home';
    this.viewData = {};
    this.history = ['home'];
    this.historyIndex = 0;
  }

  /**
   * Register a route with its render function
   */
  register(name, renderFn) {
    this.routes.set(name, renderFn);
  }

  /**
   * Navigate to a specific view
   */
  navigate(view, data = {}) {
    const renderFn = this.routes.get(view);
    
    if (!renderFn) {
      console.error(`Route "${view}" not found`);
      return;
    }

    // Update history
    this.history = this.history.slice(0, this.historyIndex + 1);
    this.history.push(view);
    this.historyIndex = this.history.length - 1;

    // Update current view
    this.currentView = view;
    this.viewData = data;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Render the view
    this.render();
  }

  /**
   * Go back in history
   */
  back() {
    if (this.historyIndex > 0) {
      this.historyIndex--;
      this.currentView = this.history[this.historyIndex];
      this.viewData = {};
      this.render();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  /**
   * Render current view
   */
  render() {
    const renderFn = this.routes.get(this.currentView);
    
    if (renderFn) {
      const appContainer = document.getElementById('app');
      if (appContainer) {
        // Add fade out animation
        appContainer.style.opacity = '0';
        
        setTimeout(() => {
          // Clear and render new content
          appContainer.innerHTML = '';
          renderFn(this.viewData, appContainer);
          
          // Fade in
          requestAnimationFrame(() => {
            appContainer.style.opacity = '1';
          });
        }, 150);
      }
    }
  }

  /**
   * Get current view name
   */
  getCurrentView() {
    return this.currentView;
  }

  /**
   * Get view data
   */
  getViewData() {
    return this.viewData;
  }
}

// Create and export global router instance
const router = new Router();
window.router = router;

export default router;
