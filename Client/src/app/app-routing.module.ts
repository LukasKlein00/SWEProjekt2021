import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BuilderComponent } from './builder/builder.component';
import { HomeComponent } from './home/home.component';
import { ImpressumComponent } from './impressum/impressum.component';
import { LoginComponent } from './login/login.component';
import { PlayComponent } from './play/play.component';
import { ProfilComponent } from './profil/profil.component';
import { RegisterComponent } from './register/register.component';
import { AuthguardService } from './services/authguard.service';
import { TestComponent } from './test/test.component';



const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'test', component: TestComponent, canActivate: [AuthguardService] },
  { path: 'play', component: PlayComponent, canActivate: [AuthguardService] },
  { path: 'impressum', component: ImpressumComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'builder', component: BuilderComponent, canActivate: [AuthguardService] },
  { path: 'profil', component: ProfilComponent, canActivate: [AuthguardService] },

  { path: '**', component: TestComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
