import { Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { UsersService } from '../users/users.service';
import * as nacl from 'tweetnacl';
import { PublicKey } from '@solana/web3.js';
import * as crypto from 'crypto';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class AuthService {
  private readonly privateKey: crypto.KeyObject;
  private readonly publicKey: crypto.KeyObject;

  constructor(
    private usersService: UsersService,
    private jwtService: JwtService,
    private configService: ConfigService,
  ) {
    this.privateKey = crypto.createPrivateKey({
      key: Buffer.from(
        this.configService.get<string>('PRIVATE_KEY_BASE64'),
        'base64',
      ),
      format: 'pem',
    });
    this.publicKey = crypto.createPublicKey({
      key: Buffer.from(
        this.configService.get<string>('PUBLIC_KEY_BASE64'),
        'base64',
      ),
      format: 'pem',
    });
  }

  async generateAuthMessage() {
    const timestamp = Date.now().toString();
    const maxLength = 117 - timestamp.length - 1;
    const randomPart = crypto
      .randomBytes(maxLength)
      .toString('base64')
      .slice(0, maxLength);
    const originalMessage = `${timestamp}_${randomPart}`;

    const encryptedMessage = crypto.publicEncrypt(
      {
        key: this.publicKey,
        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      },
      Buffer.from(originalMessage),
    );

    return {
      encryptedMessage: "Sign to make comments: "+encryptedMessage.toString('base64'),
      originalMessage,
    };
  }

  async validateUser(
    walletAddress: string,
    signedMessage: string,
    encryptedMessage: string,
  ): Promise<any> {
    console.log('Validating user with:', {
      walletAddress,
      signedMessage,
      encryptedMessage,
    });

    let user = await this.usersService.findOne(walletAddress);
    if (!user) {
      user = await this.usersService.create(walletAddress);
    }

    const publicKey = new PublicKey(walletAddress);
    console.log('Public key:', publicKey.toBase58());

    const signedMessageBuffer = Buffer.from(signedMessage, 'base64');
    const encryptedMessageBuffer = Buffer.from(encryptedMessage, 'base64');

    console.log('Signed message buffer:', signedMessageBuffer.toString('hex'));
    console.log(
      'Encrypted message buffer:',
      encryptedMessageBuffer.toString('hex'),
    );

    try {
      const messageUint8 = new TextEncoder().encode(encryptedMessage);
      const isValid = nacl.sign.detached.verify(
        messageUint8,
        signedMessageBuffer,
        publicKey.toBytes(),
      );
      console.log('Signature verification result:', isValid);

      if (!isValid) {
        throw new Error('Signature verification failed');
      }

      const decryptedMessage = crypto.privateDecrypt(
        {
          key: this.privateKey,
          padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        },
        encryptedMessageBuffer,
      );

      const messageTimestamp = parseInt(
        decryptedMessage.toString().split('_')[0],
      );
      const timeDifference = Date.now() - messageTimestamp;

      if (timeDifference > 30000) {
        throw new Error('Message expired');
      }

      await this.usersService.updateLastSignedIn(walletAddress);
      return user;
    } catch (error) {
      console.error('Error during signature verification:', error);
      throw error;
    }
  }

  async login(user: any) {
    const payload = { walletAddress: user.walletAddress, sub: user._id };
    return {
      access_token: this.jwtService.sign(payload),
    };
  }
}
