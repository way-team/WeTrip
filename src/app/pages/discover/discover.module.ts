import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';
import { IonicModule } from '@ionic/angular';

import { PopmenuComponent } from './../../components/popmenu/popmenu.component';

import { DiscoverPage } from './discover.page';
// Componentes externos que realizan peticiones
import { HttpClient } from '@angular/common/http';
import { TranslateModule, TranslateLoader } from '@ngx-translate/core';

// Configuración de traducción
import { HttpLoaderFactory } from './../../app.module';
import { BannerComponent } from 'src/app/components/banner/banner.component';
const routes: Routes = [
  {
    path: '',
    component: DiscoverPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    IonicModule,
    TranslateModule,
    RouterModule.forChild(routes)
  ],
  declarations: [DiscoverPage, PopmenuComponent, BannerComponent]
})
export class DiscoverPageModule {}
