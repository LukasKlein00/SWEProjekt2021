import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BuilderComponent } from './builder/builder.component';
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
  { path: 'builder', component: BuilderComponent },

  { path: '**', component: TestComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
