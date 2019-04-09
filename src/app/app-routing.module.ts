import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  { path: '', loadChildren: './pages/login/login.module#LoginPageModule' },
  {
    path: 'register',
    loadChildren: './pages/register/register.module#RegisterPageModule'
  },
  {
    path: 'about',
    loadChildren: './pages/about/about.module#AboutPageModule',
    canLoad: [AuthGuard]
  },
  {
    path: 'contacts',
    loadChildren: './pages/contacts/contacts.module#ContactsPageModule',
    canLoad: [AuthGuard]
  },
  {
    path: 'settings',
    loadChildren: './pages/settings/settings.module#SettingsPageModule',
    canLoad: [AuthGuard]
  },
  {
    path: 'edit-profile/:id',
    loadChildren:
      './pages/edit-profile/edit-profile.module#EditProfilePageModule',
    canLoad: [AuthGuard]
  },
  {
    path: 'discover',
    loadChildren: './pages/discover/discover.module#DiscoverPageModule',
    canLoad: [AuthGuard]
  },
  {
    path: 'trip-detail/:id',
    loadChildren: './pages/trip-detail/trip-detail.module#TripdetailPageModule',
    canLoad: [AuthGuard]
  },
  {
    path: 'chat',
    children: [
      {
        path: ':loggedUsername',
        children: [
          {
            path: ':otherUsername',
            loadChildren: './pages/chat/chat.module#ChatPageModule',
            canLoad: [AuthGuard]
          }
        ]
      }
    ]
  },
  {
    path: 'premium',
    loadChildren: './pages/premium/premium.module#PremiumPageModule',
    canLoad: [AuthGuard]
  },
  {
    path: 'trips',
    loadChildren: './pages/trips/trips.module#TripsPageModule',
    canLoad: [AuthGuard]
  },
  {
    path: 'search',
    loadChildren: './pages/search/search.module#SearchPageModule',
    canLoad: [AuthGuard]
  },
  {
    path: 'user-profile/:username',
    loadChildren:
      './pages/user-profile/user-profile.module#UserProfilePageModule',
    canLoad: [AuthGuard]
  },
  {
    path: 'create-trip',
    loadChildren: './pages/create-trip/create-trip.module#CreateTripPageModule'
  },
  {
    path: 'create-trip/:id',
    loadChildren: './pages/create-trip/create-trip.module#CreateTripPageModule'
  },
  {
    path: 'gdpr',
    loadChildren: './pages/gdpr/gdpr.module#GdprPageModule'
  },
  {
    path: 'search',
    loadChildren: './pages/search/search.module#SearchPageModule'
  },
  {
    path: 'rating/:username',
    loadChildren: './pages/rating/rating.module#RatingPageModule',
    canLoad: [AuthGuard]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
