import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import { setupLoadingInterceptors } from './services/api';

const app = createApp(App);
app.use(router);
app.use(store);
setupLoadingInterceptors(store);
store.dispatch('initialize');
app.use(vuetify);
app.mount('#app');
