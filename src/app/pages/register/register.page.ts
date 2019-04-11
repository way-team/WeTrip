import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  Validators,
  EmailValidator
} from '@angular/forms';
import {
  NavController,
  MenuController,
  LoadingController,
  AlertController
} from '@ionic/angular';
import { Language, Interest } from 'src/app/app.data.model';
import { DataManagement } from 'src/app/services/dataManagement';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss']
})
export class RegisterPage implements OnInit {
  public onRegisterForm: FormGroup;
  username: string;
  password: string;
  confirmPassword: string;
  email: string;
  first_name: string;
  last_name: string;
  description: string;
  birthdate: string;
  gender: string;
  nationality: string;
  city: string;
  languages;
  languagesOptions: Language[];
  interests;
  interestsOptions: Interest[];
  profilePic: File = null;
  discoverPic: File = null;

  constructor(
    public navCtrl: NavController,
    public menuCtrl: MenuController,
    public loadingCtrl: LoadingController,
    private formBuilder: FormBuilder,
    public dm: DataManagement,
    public alertCtrl: AlertController
  ) {
    this.listLanguages();
    this.listInterests();
  }

  public listLanguages() {
    this.dm
      .listLanguages()
      .then(data => {
        this.languagesOptions = data;
      })
      .catch(error => {
        console.log(error);
      });
  }
  public listInterests() {
    this.dm
      .listInterests()
      .then(data => {
        this.interestsOptions = data;
      })
      .catch(error => {
        console.log(error);
      });
  }

  ionViewWillEnter() {
    this.menuCtrl.enable(false);
  }

  ngOnInit() {
    this.onRegisterForm = this.formBuilder.group({
      username: [null, Validators.compose([Validators.required])],
      password: [null, Validators.compose([Validators.required])],
      confirmPassword: [null, Validators.compose([Validators.required])],
      email: [
        null,
        Validators.compose([Validators.required, Validators.email])
      ],
      first_name: [null, Validators.compose([Validators.required])],
      last_name: [null, Validators.compose([Validators.required])],
      description: [null, Validators.compose([Validators.required])],
      birthdate: [null, Validators.compose([Validators.required])],
      gender: [null, Validators.compose([Validators.required])],
      nationality: [null, Validators.compose([Validators.required])],
      city: [null, Validators.compose([Validators.required])],
      languages: [null, Validators.compose([Validators.required])],
      interests: [null, Validators.compose([Validators.required])]
    });
  }

  confirmPasswordValidation() {
    if (this.password === this.confirmPassword) {
      return true;
    } else {
      return false;
    }
  }

  public signUp() {
    this.dm
      .register(
        this.username,
        this.password,
        this.email,
        this.first_name,
        this.last_name,
        this.description,
        this.birthdate.split('T')[0],
        this.gender,
        this.nationality,
        this.city,
        this.languages,
        this.interests,
        this.profilePic,
        this.discoverPic
      )
      .then(data => {
        this.alertCtrl
          .create({
            header: 'Succes',
            message: 'Sign up done successfully!',
            buttons: [
              {
                text: 'Ok',
                role: 'ok'
              }
            ]
          })
          .then(alertEl => {
            alertEl.present();
          });
        this.navCtrl.navigateForward('/');
        (this.username = ''),
          (this.password = ''),
          (this.confirmPassword = ''),
          (this.email = ''),
          (this.first_name = ''),
          (this.last_name = ''),
          (this.description = ''),
          (this.birthdate = ''),
          (this.gender = ''),
          (this.nationality = ''),
          (this.city = ''),
          (this.languages = ''),
          (this.interests = ''),
          (this.profilePic = null),
          (this.discoverPic = null);
      })
      .catch(error => {
        this.alertCtrl
          .create({
            header: 'Error',
            message: 'The username or email is already taken',
            buttons: [
              {
                text: 'Ok',
                role: 'ok'
              }
            ]
          })
          .then(alertEl => {
            alertEl.present();
          });
      });
  }

  // // //
  goToLogin() {
    this.navCtrl.navigateRoot('/');
  }

  onProfilePicInputChange(file: File) {
    this.profilePic = file[0];
  }

  onDiscoverPicInputChange(file: File) {
    this.discoverPic = file[0];
  }
  validateBirthdate() {
    const birthdate = new Date(this.birthdate);
    const today = new Date();

    if (birthdate > today) {
      return false;
    }
    return true;
  }
}
