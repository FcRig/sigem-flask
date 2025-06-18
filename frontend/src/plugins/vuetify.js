import { createVuetify } from 'vuetify';
import 'vuetify/styles';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'customLight',
    themes: {
      customLight: {
        dark: false,
        colors: {
          primary: '#002776',
          secondary: '#FFCC00',
          accent: '#FFFFFF'
        }
      }
    }
  }
});
