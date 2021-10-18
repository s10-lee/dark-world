// import BBtn from './BBtn';
// import BLink from './BLink';
// import BInput from './BInput';
// import BLabel from './BLabel';
// import BNavbar from './BNavbar'
// import BLoading from './BLoading';

// () => import('pages/payment/success')
// files.keys().map(function (key) {
//     app.component(key.split('/').pop().split('.')[0], files(key).default);
// });


export const registerComponents = (app) => {
    const files = require.context('./', true, /.vue$/i);
    files.keys().map(key => {
        app.component(key.split('/').pop().split('.')[0], files(key).default);
    });
}
