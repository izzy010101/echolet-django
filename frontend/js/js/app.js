// frontend/js/app.js (or main.js)
import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import '../css/app.css';

// Define your app name. You can pass this from Django as a prop if it's dynamic.
const appName = window.document.getElementsByTagName('title')[0]?.innerText || 'My Django App';

createInertiaApp({
    title: (title) => `${title} - ${appName}`,

    resolve: (name) => {
        const pages = import.meta.glob('../js/Pages/**/*.vue', { eager: true });
        const path = `./Pages/${name}.vue`;

        if (!pages[path]) {
            throw new Error(`Inertia: Component not found for name "${name}". Expected path: "${path}".`);
        }

        return pages[path].default;
    },

    setup({ el, App, props, plugin }) {
        return createApp({ render: () => h(App, props) })
            .use(plugin)
            .mount(el);
    },
    progress: {
        color: '#4B5563',
    },
});