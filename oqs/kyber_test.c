/**
 * Kyber Key Exchange Test - Quantum-Safe Cryptography
 * 
 * This test demonstrates a complete key exchange using Kyber-768,
 * a NIST-approved post-quantum cryptographic algorithm (FIPS 203 - ML-KEM).
 * 
 * The test simulates a key exchange between two parties (Alice and Bob):
 * 1. Alice generates a keypair
 * 2. Bob encapsulates a shared secret using Alice's public key
 * 3. Alice decapsulates to recover the same shared secret
 * 4. Both parties verify they have the same shared secret
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <oqs/oqs.h>

#define KYBER_VARIANT "Kyber768"

void print_hex(const char *label, const uint8_t *data, size_t len) {
    printf("%s: ", label);
    for (size_t i = 0; i < (len > 32 ? 32 : len); i++) {
        printf("%02x", data[i]);
    }
    if (len > 32) {
        printf("... (%zu bytes total)", len);
    }
    printf("\n");
}

int main(void) {
    printf("========================================\n");
    printf("Kyber-768 Key Exchange Test\n");
    printf("Post-Quantum Cryptography (NIST FIPS 203)\n");
    printf("========================================\n\n");

    // Initialize the Kyber-768 KEM
    OQS_KEM *kem = OQS_KEM_new(OQS_KEM_alg_kyber_768);
    if (kem == NULL) {
        fprintf(stderr, "ERROR: OQS_KEM_new failed for %s\n", KYBER_VARIANT);
        fprintf(stderr, "Make sure liboqs is properly installed with Kyber support.\n");
        return EXIT_FAILURE;
    }

    printf("Algorithm: %s\n", kem->method_name);
    printf("NIST Security Level: %d\n", kem->claimed_nist_level);
    printf("Public Key Size: %zu bytes\n", kem->length_public_key);
    printf("Secret Key Size: %zu bytes\n", kem->length_secret_key);
    printf("Ciphertext Size: %zu bytes\n", kem->length_ciphertext);
    printf("Shared Secret Size: %zu bytes\n\n", kem->length_shared_secret);

    // Allocate memory for keys and secrets
    uint8_t *public_key = malloc(kem->length_public_key);
    uint8_t *secret_key = malloc(kem->length_secret_key);
    uint8_t *ciphertext = malloc(kem->length_ciphertext);
    uint8_t *shared_secret_alice = malloc(kem->length_shared_secret);
    uint8_t *shared_secret_bob = malloc(kem->length_shared_secret);

    if (!public_key || !secret_key || !ciphertext || 
        !shared_secret_alice || !shared_secret_bob) {
        fprintf(stderr, "ERROR: Memory allocation failed\n");
        OQS_KEM_free(kem);
        return EXIT_FAILURE;
    }

    printf("Step 1: Alice generates keypair\n");
    printf("-----------------------------------\n");
    OQS_STATUS rc = OQS_KEM_keypair(kem, public_key, secret_key);
    if (rc != OQS_SUCCESS) {
        fprintf(stderr, "ERROR: OQS_KEM_keypair failed\n");
        goto cleanup;
    }
    print_hex("Public Key", public_key, kem->length_public_key);
    print_hex("Secret Key", secret_key, kem->length_secret_key);
    printf("✓ Keypair generated successfully\n\n");

    printf("Step 2: Bob encapsulates shared secret\n");
    printf("-----------------------------------\n");
    printf("Bob uses Alice's public key to create a shared secret\n");
    rc = OQS_KEM_encaps(kem, ciphertext, shared_secret_bob, public_key);
    if (rc != OQS_SUCCESS) {
        fprintf(stderr, "ERROR: OQS_KEM_encaps failed\n");
        goto cleanup;
    }
    print_hex("Ciphertext", ciphertext, kem->length_ciphertext);
    print_hex("Bob's Shared Secret", shared_secret_bob, kem->length_shared_secret);
    printf("✓ Encapsulation successful\n\n");

    printf("Step 3: Alice decapsulates shared secret\n");
    printf("-----------------------------------\n");
    printf("Alice uses her secret key to recover the shared secret\n");
    rc = OQS_KEM_decaps(kem, shared_secret_alice, ciphertext, secret_key);
    if (rc != OQS_SUCCESS) {
        fprintf(stderr, "ERROR: OQS_KEM_decaps failed\n");
        goto cleanup;
    }
    print_hex("Alice's Shared Secret", shared_secret_alice, kem->length_shared_secret);
    printf("✓ Decapsulation successful\n\n");

    printf("Step 4: Verify shared secrets match\n");
    printf("-----------------------------------\n");
    if (memcmp(shared_secret_alice, shared_secret_bob, kem->length_shared_secret) == 0) {
        printf("✓ SUCCESS: Both parties have the same shared secret!\n");
        printf("✓ Key exchange completed successfully\n");
        printf("\nThis shared secret can now be used for symmetric encryption.\n");
        rc = OQS_SUCCESS;
    } else {
        fprintf(stderr, "✗ FAILURE: Shared secrets do not match!\n");
        rc = OQS_ERROR;
    }

    printf("\n========================================\n");
    printf("Kyber-768 is quantum-resistant and provides\n");
    printf("security equivalent to AES-192 against both\n");
    printf("classical and quantum computers.\n");
    printf("========================================\n");

cleanup:
    // Clean up and securely clear sensitive cryptographic material
    if (secret_key) {
        memset(secret_key, 0, kem->length_secret_key);
        free(secret_key);
    }
    if (shared_secret_alice) {
        memset(shared_secret_alice, 0, kem->length_shared_secret);
        free(shared_secret_alice);
    }
    if (shared_secret_bob) {
        memset(shared_secret_bob, 0, kem->length_shared_secret);
        free(shared_secret_bob);
    }
    free(public_key);
    free(ciphertext);
    OQS_KEM_free(kem);

    return (rc == OQS_SUCCESS) ? EXIT_SUCCESS : EXIT_FAILURE;
}
