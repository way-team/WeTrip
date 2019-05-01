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
import { TranslateService } from '@ngx-translate/core';

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
  profesion: string;
  civilStatus: string;
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
    private translate: TranslateService,
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
      profesion: [null, null],
      civilStatus: [null, Validators.compose([Validators.required])],
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
    let translation1: string = this.translate.instant('REGISTER.HEADER_SUCCESS');
    let translation2: string = this.translate.instant('REGISTER.SUCCESS');
    let translation3: string = this.translate.instant('REGISTER.ERROR_USERNAME');

    this.dm.register(
      this.username,
      this.password,
      this.email,
      this.first_name,
      this.last_name,
      this.description,
      this.birthdate.split('T')[0],
      this.profesion,
      this.civilStatus,
      this.gender,
      this.nationality,
      this.city,
      this.languages,
      this.interests,
      this.profilePic,
      this.discoverPic
    ).then(data => {
      this.showLoading();
      setTimeout(() => {
        this.alertCtrl
          .create({
            header: translation1,
            message: translation2,
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
      }, 1500);
    })
      .catch(error => {
        this.showLoading();
        setTimeout(() => {
          this.alertCtrl
            .create({
              header: 'Error',
              message: translation3,
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
        }, 1500);
      });
  }
  showLoading() {
    const translation2: string = this.translate.instant('DISCOVER.WAIT');
    this.loadingCtrl
      .create({
        message: translation2,
        showBackdrop: true,
        duration: 1000
      })
      .then(loadingEl => {
        loadingEl.present();
      });
  }

  // // //
  goToLogin() {
    this.navCtrl.navigateRoot('/');
  }

  onProfilePicInputChange(file: File) {
    this.checkFileIsImage(file[0], 'profPic');
    this.profilePic = file[0];
  }

  onDiscoverPicInputChange(file: File) {
    this.checkFileIsImage(file[0], 'dicPic');
    this.discoverPic = file[0];
  }

  private checkFileIsImage(file: File, picture: string) {
    if (!(file.type.split('/')[0] == 'image')) {
      let translation1: string = this.translate.instant('REGISTER.IMAGE_ERROR');

      this.alertCtrl
        .create({
          header: translation1,
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

      if (picture == 'profPic') {
        this.profilePic = null;
        // Aunque de fallo de compilación, funciona
        document.getElementById('procPic').value = "";
      }

      if (picture == 'dicPic') {
        this.discoverPic = null;
        // Aunque de fallo de compilación, funciona
        document.getElementById('dicoverPic').value = "";
      }
    }






  }

  validateBirthdate() {
    const birthdate = new Date(this.birthdate);
    const today = new Date();
    this.isAdult(birthdate);

    if (birthdate > today || !this.isAdult(birthdate)) {
      return false;
    }
    return true;
  }

  private isAdult(birthdate: Date): boolean {
    const today = new Date();
    const today_year = today.getFullYear();
    const today_month = today.getMonth() + 1;
    const today_day = today.getDate();

    let edad = today_year + 1900 - birthdate.getFullYear();
    if (today_month < birthdate.getMonth()) {
      edad--;
    }
    if (
      birthdate.getMonth() == today_month &&
      today_day < birthdate.getDate()
    ) {
      edad--;
    }
    if (edad > 1900) {
      edad -= 1900;
    }

    // calculamos los meses
    let meses = 0;

    if (today_month > birthdate.getMonth() && birthdate.getDate() > today_day) {
      meses = today_month - birthdate.getMonth() - 1;
    } else if (today_month > birthdate.getMonth()) {
      meses = today_month - birthdate.getMonth();
    }

    if (today_month < birthdate.getMonth() && birthdate.getDate() < today_day) {
      meses = 12 - (birthdate.getMonth() - today_month);
    } else if (today_month < birthdate.getMonth()) {
      meses = 12 - (birthdate.getMonth() - today_month + 1);
    }

    if (
      today_month == birthdate.getMonth() &&
      birthdate.getDate() > today_day
    ) {
      meses = 11;
    }
    // calculamos los dias
    let dias = 0;
    if (today_day > birthdate.getDate()) {
      dias = today_day - birthdate.getDate();
    }

    if (today_day < birthdate.getDate()) {
      let ultimoDiaMes = new Date(today_year, today_month - 1, 0);
      dias = ultimoDiaMes.getDate() - (birthdate.getDate() - today_day);
    }

    return edad > 18;
  }
}
