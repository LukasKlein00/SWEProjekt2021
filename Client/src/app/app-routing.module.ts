import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ImpressumComponent } from './impressum/impressum.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { AuthguardService } from './services/authguard.service';
import { TestComponent } from './test/test.component';



const routes: Routes = [
  { path: '', component: TestComponent },
  { path: 'impressum', component: ImpressumComponent },
  { path: 'play', component: ImpressumComponent, canActivate: [AuthguardService] },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },

  { path: '**', component: TestComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
