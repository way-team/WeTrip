import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { IonicModule } from '@ionic/angular';

import { TripsPage } from './trips.page';
import { BannerModule } from 'src/app/components/banner/banner.module';

const routes: Routes = [
  {
    path: '',
    component: TripsPage
  }
];

@NgModule({
  imports: [
    BannerModule,
    CommonModule,
    FormsModule,
    IonicModule,
    TranslateModule,
    RouterModule.forChild(routes)
  ],
  declarations: [TripsPage]
})
export class TripsPageModule {}
