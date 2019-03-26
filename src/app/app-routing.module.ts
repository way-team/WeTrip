import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
  { path: '', loadChildren: './pages/login/login.module#LoginPageModule' },
  { path: 'register', loadChildren: './pages/register/register.module#RegisterPageModule' },
  { path: 'about', loadChildren: './pages/about/about.module#AboutPageModule' },
  { path: 'contacts', loadChildren: './pages/contacts/contacts.module#ContactsPageModule' },
  { path: 'settings', loadChildren: './pages/settings/settings.module#SettingsPageModule' },
  { path: 'edit-profile/:id', loadChildren: './pages/edit-profile/edit-profile.module#EditProfilePageModule' },
  { path: 'discover', loadChildren: './pages/discover/discover.module#DiscoverPageModule' },
  { path: 'trip-detail', loadChildren: './pages/trip-detail/trip-detail.module#TripdetailPageModule' },
  { path: 'chat/:id', loadChildren: './pages/chat/chat.module#ChatPageModule' },
  { path: 'premium', loadChildren: './pages/premium/premium.module#PremiumPageModule' },
  { path: 'user-profile', loadChildren: './pages/user-profile/user-profile.module#UserProfilePageModule' }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule {}
