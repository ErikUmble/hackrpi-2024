import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [  
  
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'), // Layout component
    children: [
      //{ path: 'about', component: () => import('pages/AboutPage.vue') }, // About page
      { path: '', component: () => import('pages/IndexPage.vue') }, // Home page
    ]
  },
  

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
