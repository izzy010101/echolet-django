// frontend/js/app.js 
import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import '../css/app.css';

const appName = document.title || 'Echolet App';

createInertiaApp({
    title: (title) => `${title} - ${appName}`,

    resolve: (name) => {
        const pages = import.meta.glob('./Pages/**/*.vue', { eager: true }); // ✅ RELATIVE TO js/
        const path = `./Pages/${name}.vue`; // ✅ matches the glob keys exactly

        if (!pages[path]) {
            console.error('Available pages:', Object.keys(pages)); // for debugging
            throw new Error(`Inertia: Component "${name}" not found. Expected path: "${path}"`);
        }

        return pages[path].default;
    },

    setup({ el, App, props, plugin }) {
        createApp({ render: () => h(App, props) })
            .use(plugin)
            .mount(el);
    },

    progress: {
        color: '#4B5563',
    },
});
